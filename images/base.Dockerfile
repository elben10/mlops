FROM python:3.11

RUN pip install git+https://github.com/python-poetry/poetry git+https://github.com/python-poetry/poetry-core && \
    poetry config virtualenvs.create false

WORKDIR /src

COPY src ./src

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY images/entrypoints /entrypoints