#!/usr/bin/env bash

set -e

# Get the actual version to use:
LIB_VERSION=$(dunamai from git --style pep440 --no-metadata)
# Bump library version:
echo "Publishing version $LIB_VERSION."
poetry version $LIB_VERSION

# https://python-poetry.org/docs/libraries/
# https://python-poetry.org/docs/cli/#publish
poetry publish --build
