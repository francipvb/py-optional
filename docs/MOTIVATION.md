# Motivation

**TLDR**:

> This is inspired by java **Option** object and dart [optional] package.

## Objective

When writing updateable resources, sometimes you only want a subset of the data to be changed. This is not an issue if the data shouldn't be `None` value. However, there are cases when the data can be `None` and you must ensure the value were not provided.

You can, of course, use a sentinel object as function's default values, but then you are issues with the typing support.

This is why I coded this simple, trivial construction for the python community.

[optional]: https://pub.dev/packages/optional
