#!/usr/bin/env bash

set -e

mlops-utils database create --uri postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${DAGSTER_DATABASE}

exec dagit \
    -h 0.0.0.0 \
    -p 3000 \
    -w config/dagster/workspace.yaml