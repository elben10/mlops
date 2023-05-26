import os

from sqlalchemy_utils import create_database, database_exists
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(stop=stop_after_attempt(60), wait=wait_fixed(1))
def main():
    if not database_exists(os.environ.get("MLFLOW_BACKEND_STORE_URI")):
        create_database(os.environ.get("MLFLOW_BACKEND_STORE_URI"))


if __name__ == "__main__":
    main()
