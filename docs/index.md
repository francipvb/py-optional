# py-optional

## Introduction

This is a python implementation for optional values. Don't confuse them with `None` values because in fact thei are present.

## Features

- Supports setting values as empty.
- Implements checks for value presence or absence.
- Factory methods to create empty and valued objects are provided.
- Full typing support.

## Installation

Install the latest release:

```bash
pip install py-optional
```

Or you can clone `py-optional` and get started locally

```bash
# ensure you have Poetry installed
pip install --user poetry

# install all dependencies (including dev)
poetry install

# develop!

```

## Example Usage

```python
# Import it with an alias
from optional import Optional as O

# This is the main purpose of the library, so define a function
def sum_numbers(*, a: O[int] = O.empty(), b: O[int] = O.empty()):
    # Check if the two numbers are empty:
    if a.is_empty and b.is_empty:
        raise ValueError('No numbers were provided.')

    # The `or_else` method returns either the default value or the wrapped value:
    return a.or_else(0) + b.or_else(0)

# Sum an int with nothing:
print(sum_numbers(a=O.of(3), b=O.of(5))) # -> 8
```

Only **Python 3.8+** is supported as required by the black, pydantic packages

When you make a release on GitHub, the publish workflow will run and deploy to PyPi! 🚀🎉😎
