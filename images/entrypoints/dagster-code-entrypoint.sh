#!/usr/bin/env bash

set -e

exec dagster api grpc \
    --host 0.0.0.0 \
    --port 4266 \
    --module-name mlops.etl
