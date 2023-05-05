#!/usr/bin/env bash

set -e

if [ -z "$1" ]
  then
    pytest tests
  else
    pytest tests $@
fi