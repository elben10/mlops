from datetime import datetime
import io
import json

from botocore.exceptions import ClientError
from dagster import (
    AutoMaterializePolicy,
    OpExecutionContext,
    MonthlyPartitionsDefinition,
    asset,
    graph_asset,
    op,
)
from sqlalchemy.dialects.postgresql import insert

bucket_name = "energy-data"
strf_format = "%Y-%m-%dT%H:%M"


@op(required_resource_keys={"s3"})
def create_bucket(context: OpExecutionContext) -> str:
    try:
        context.resources.s3.head_bucket(Bucket=bucket_name)
    except ClientError:
        context.resources.s3.create_bucket(Bucket=bucket_name)
    return bucket_name


@op(required_resource_keys={"energy_data", "s3"})
def save_data(context: OpExecutionContext, bucket_name: str) -> None:
    offset = 0
    limit = 1000
    initial = True
    records = []
    while initial or limit == len(r.json()["records"]):
        if initial:
            initial = False
        r = context.resources.energy_data.get_client().get(
            "/dataset/Elspotprices",
            params={
                "offset": offset,
                "limit": limit,
                "start": context.partition_time_window.start.strftime(strf_format),
                "end": context.partition_time_window.end.strftime(strf_format),
            },
        )
        records += r.json()["records"]
        offset += limit
    context.resources.s3.upload_fileobj(
        Fileobj=io.BytesIO(json.dumps(records).encode()),
        Bucket=bucket_name,
        Key=f"{context.partition_key}.json",
    )


@graph_asset(partitions_def=MonthlyPartitionsDefinition(start_date="2020-01-01"))
def fetch_data() -> None:
    return save_data(create_bucket())


@asset(
    partitions_def=MonthlyPartitionsDefinition(start_date="2020-01-01"),
    required_resource_keys={"s3"},
    non_argument_deps={"fetch_data"},
    auto_materialize_policy=AutoMaterializePolicy.eager(),
)
def ingest_data(context: OpExecutionContext) -> None:
    from mlops.etl.database import EnergyData, Session

    key = f"{context.partition_key}.json"
    fileobj = io.BytesIO()
    context.resources.s3.download_fileobj(Bucket=bucket_name, Key=key, Fileobj=fileobj)
    fileobj.seek(0)
    data = json.loads(fileobj.read().decode())
    objs = [
        dict(
            time=datetime.fromisoformat(record["HourUTC"]),
            price_area=record["PriceArea"],
            spotprice_dkk=record["SpotPriceDKK"],
            spotprice_eur=record["SpotPriceEUR"],
        )
        for record in data
    ]
    with Session() as session:
        stmt = insert(EnergyData).values(objs)
        stmt = stmt.on_conflict_do_update(
            constraint="energydata_time_price_area_key",
            set_={
                "spotprice_dkk": stmt.excluded.spotprice_dkk,
                "spotprice_eur": stmt.excluded.spotprice_eur,
            },
        )
        session.execute(stmt)


@asset(
    partitions_def=MonthlyPartitionsDefinition(start_date="2020-01-01"),
    auto_materialize_policy=AutoMaterializePolicy.eager(),
    non_argument_deps={"ingest_data"},
)
def materialize_features() -> None:
    from feast import FeatureStore

    from mlops.etl.energy_data.features import (
        price_area,
        energy_data_fv,
    )

    fs = FeatureStore("config/feast")
    fs.apply([price_area, energy_data_fv])
    fs.materialize_incremental(end_date=datetime.utcnow())
