from httpx import Client
from dagster import ConfigurableResource, EnvVar
from dagster_aws.s3 import S3Resource


class EnergyData(ConfigurableResource):
    def get_client(self):
        return Client(base_url="https://api.energidataservice.dk")


energy_data = EnergyData()
s3 = S3Resource(
    endpoint_url=EnvVar("S3_ENDPOINT"),
    aws_access_key_id=EnvVar("S3_ACCESS_KEY"),
    aws_secret_access_key=EnvVar("S3_SECRET_KEY"),
)
