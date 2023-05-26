#!/usr/bin/env bash

set -e

exec dagster-daemon run \
    -w config/dagster/workspace.yaml