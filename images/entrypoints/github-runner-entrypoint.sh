#!/usr/bin/env bash

set -e

./config.sh --ephemeral --unattended --url $URL --token $TOKEN
./run.sh
./config.sh remove --token "$TOKEN"