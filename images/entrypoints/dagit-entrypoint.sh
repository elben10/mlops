#!/usr/bin/env bash

set -e

mlops-utils database create --uri postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DATABASE}

exec dagit \
    -h 0.0.0.0 \
    -p 3000 \
    --grpc-host dagster-code \
    --grpc-port 4266