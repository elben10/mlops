#/usr/bin/env bash

set -e

mlops-utils database create --uri $MLFLOW_BACKEND_STORE_URI

exec mlflow server