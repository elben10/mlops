#!/usr/bin/env bash

set -e 

mlops-utils database create --uri postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DATABASE}

exec feast ui --host 0.0.0.0 --port 8020