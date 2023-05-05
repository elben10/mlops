#!/usr/bin/env bash

set -e

if [ -z "$1" ]
  then
    pytest
  else
    pytest $@
fi