FROM python:3.11

RUN pip install git+https://github.com/python-poetry/poetry && \
    poetry config virtualenvs.create false

WORKDIR /src

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-directory

COPY src ./src

RUN poetry install 

COPY images/entrypoints /entrypoints