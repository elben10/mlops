from sqlalchemy_utils import create_database, database_exists
from tenacity import retry, stop_after_attempt, wait_fixed
from typer import Typer, Option

app = Typer()
app_database = Typer()


@app_database.command(name="create")
@retry(stop=stop_after_attempt(60), wait=wait_fixed(1))
def hello(uri: str = Option(...)):
    if not database_exists(uri):
        print("Creating database")
        create_database(uri)


app.add_typer(app_database, name="database")

if __name__ == "__main__":
    app()
