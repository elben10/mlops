from unittest import mock

import httpx
import pytest
import tenacity
from dagster import materialize, materialize_to_memory

from mlops.etl.energy_data.assets import fetch_data, ingest_data


@pytest.mark.unit
def test_unit():
    result = materialize_to_memory(
        [fetch_data],
        resources={
            "energy_data": mock.MagicMock(
                get_client=lambda: mock.MagicMock(
                    get=lambda *args, **kwargs: mock.MagicMock(
                        json=lambda: {
                            "total": 1668183,
                            "sort": "HourUTC DESC",
                            "limit": 100,
                            "dataset": "Elspotprices",
                            "records": [
                                {
                                    "HourUTC": "2023-05-21T21:00:00",
                                    "HourDK": "2023-05-21T23:00:00",
                                    "PriceArea": "DK1",
                                    "SpotPriceDKK": 572.799988,
                                    "SpotPriceEUR": 76.910004,
                                },
                                {
                                    "HourUTC": "2023-05-21T21:00:00",
                                    "HourDK": "2023-05-21T23:00:00",
                                    "PriceArea": "DK2",
                                    "SpotPriceDKK": 572.799988,
                                    "SpotPriceEUR": 76.910004,
                                },
                            ],
                        }
                    )
                )
            ),
            "s3": mock.MagicMock(),
        },
        partition_key="2022-01-01",
    )

    assert result.success


@pytest.mark.integration
def test_integration():
    from mlops.etl.energy_data.assets import fetch_data, ingest_data
    from mlops.etl.energy_data.resources import energy_data, s3

    result = materialize(
        [fetch_data, ingest_data],
        resources={"energy_data": energy_data, "s3": s3},
        partition_key="2021-01-01",
    )
    assert result.success


@pytest.mark.e2e
@tenacity.retry(stop=tenacity.stop_after_attempt(60 * 1), wait=tenacity.wait_fixed(1))
def test_mlflow_available():
    try:
        httpx.get("https://mlflow.localhost", verify=False).status_code == 200
    except Exception as e:
        print(e)
        raise e


@pytest.mark.e2e
@tenacity.retry(stop=tenacity.stop_after_attempt(60 * 1), wait=tenacity.wait_fixed(1))
def test_dagit_available():
    try:
        httpx.get("https://dagit.localhost", verify=False).status_code == 200
    except Exception as e:
        print(e)
        raise e


@pytest.mark.e2e
@tenacity.retry(stop=tenacity.stop_after_attempt(60 * 1), wait=tenacity.wait_fixed(1))
def test_feast_available():
    try:
        httpx.get("https://feast.localhost", verify=False).status_code == 200
    except Exception as e:
        print(e)
        raise e


@pytest.mark.e2e
@tenacity.retry(stop=tenacity.stop_after_attempt(60 * 1), wait=tenacity.wait_fixed(1))
def test_ray_available():
    try:
        httpx.get("https://ray.localhost", verify=False).status_code == 200
    except Exception as e:
        print(e)
        raise e
