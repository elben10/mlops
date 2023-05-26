from dagster import Definitions

from mlops.etl.energy_data.assets import fetch_data, ingest_data, materialize_features
from mlops.etl.energy_data.resources import energy_data, s3

defs = Definitions(
    assets=[fetch_data, ingest_data, materialize_features],
    resources={"energy_data": energy_data, "s3": s3},
)
