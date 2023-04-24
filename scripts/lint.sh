#!/usr/bin/env bash

set -e
set -x

mypy optional --disallow-untyped-defs
black optional tests --check
isort --check-only optional tests
