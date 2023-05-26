from feast import Entity, Feature, FeatureView, Field
from feast.infra.offline_stores.contrib.postgres_offline_store.postgres_source import (
    PostgreSQLSource,
)
from feast.types import Float32

price_area = Entity(name="price_area", join_keys=["price_area"])

energy_data_source = PostgreSQLSource(
    name="energy_data", query="SELECT * FROM energydata", timestamp_field="time"
)

energy_data_fv = FeatureView(
    name="energy_data",
    entities=[price_area],
    schema=[
        Field(name="spotprice_dkk", dtype=Float32),
        Field(name="spotprice_eur", dtype=Float32),
    ],
    source=energy_data_source,
)
