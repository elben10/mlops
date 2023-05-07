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
@tenacity.retry(stop=tenacity.stop_after_attempt(60 * 5), wait=tenacity.wait_fixed(1))
def test_e2e():
    try:
        httpx.get("http://localhost").status_code == 404
    except Exception as e:
        print(e)
        raise e
