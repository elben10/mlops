FROM python:3.11-slim

RUN pip install poetry && \
    poetry config virtualenvs.create false

WORKDIR /src

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-directory

COPY src ./src

RUN poetry install 

COPY images/entrypoints /entrypoints
COPY config /src/config