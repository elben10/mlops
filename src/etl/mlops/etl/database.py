import os

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Numeric,
    String,
    create_engine,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

_user = os.environ["POSTGRES_USER"]
_password = os.environ["POSTGRES_PASSWORD"]
_host = os.environ["POSTGRES_HOST"]
_database = "mlops"

uri = f"postgresql://{_user}:{_password}@{_host}/{_database}"


if not database_exists(uri):
    create_database(uri)

engine = create_engine(uri, echo=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()


class EnergyData(Base):
    __tablename__ = "energydata"
    __table_args__ = (UniqueConstraint("time", "price_area"),)

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    price_area = Column(String)
    spotprice_dkk = Column(Numeric)
    spotprice_eur = Column(Numeric)


Base.metadata.create_all(engine)
