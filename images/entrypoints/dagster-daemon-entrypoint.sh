#!/usr/bin/env bash

set -e

exec dagster-daemon run \
    --grpc-host dagster-code \
    --grpc-port 4266