#!/usr/bin/env bash

set -e

bash ./config.sh --ephemeral --unattended --url $URL --token $TOKEN
bash ./run.sh