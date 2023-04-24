#!/usr/bin/env bash

set -e

# Get the actual version to use:
LIB_VERSION=$(dunamai from git --style pep440 --no-metadata)
# Bump library version:
poetry version $LIB_VERSION

# We use github actions to publish the packages itself, so here we only build them
poetry build
