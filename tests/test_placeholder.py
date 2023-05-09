import httpx
import pytest
import tenacity


@pytest.mark.unit
def test_unit():
    pass


@pytest.mark.integration
def test_integration():
    pass


@pytest.mark.e2e
@tenacity.retry(stop=tenacity.stop_after_attempt(60 * 1), wait=tenacity.wait_fixed(1))
def test_e2e():
    try:
        httpx.get("https://localhost", verify=False).status_code == 404
    except Exception as e:
        print(e)
        raise e


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
def test_mlflow_available():
    try:
        httpx.get("https://dagit.localhost", verify=False).status_code == 200
    except Exception as e:
        print(e)
        raise e


@pytest.mark.e2e
@tenacity.retry(stop=tenacity.stop_after_attempt(60 * 1), wait=tenacity.wait_fixed(1))
def test_mlflow_available():
    try:
        httpx.get("https://feast.localhost", verify=False).status_code == 200
    except Exception as e:
        print(e)
        raise e


@pytest.mark.e2e
@tenacity.retry(stop=tenacity.stop_after_attempt(60 * 1), wait=tenacity.wait_fixed(1))
def test_mlflow_available():
    try:
        httpx.get("https://ray.localhost", verify=False).status_code == 200
    except Exception as e:
        print(e)
        raise e
