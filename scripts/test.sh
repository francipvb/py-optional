#!/usr/bin/env bash

set -e
set -x

pytest --cov=optional --cov=tests --cov-report=term-missing ${@}
coverage lcov
bash ./scripts/lint.sh
