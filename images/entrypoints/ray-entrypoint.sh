#!/usr/bin/env bash

set -e

ray start --head --dashboard-host 0.0.0.0
serve start --http-host 0.0.0.0 --http-port 8020 --http-location EveryNode
sleep infinity