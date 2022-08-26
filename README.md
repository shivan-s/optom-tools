# Project

[![Build](https://github.com/shivan-s/python-template/actions/workflows/build.yml/badge.svg)](https://github.com/shivan-s/python-template/actions/workflows/build.yml)
[![pages-build-deployment](https://github.com/shivan-s/python-template/actions/workflows/pages/pages-build-deployment/badge.svg?branch=gh-pages)](https://github.com/shivan-s/python-template/actions/workflows/pages/pages-build-deployment)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)

## About

Provide information about the project.

## Before you start on your project

Things you will need to do:

1. remake `src/project` to the name of the project (remember must be snake case)
2. change the metadata in `setup.cfg`.

## The Structure of the Project

```shell
├── auxiliary files
├── src
│   └── project
│       ├── __init__.py
│       ├── __main__.py
│       └── project files...
├── tests
    ├── __init__.py
    ├── conftest.py
    └── project test files...
```

## Tests

The technologies used include:

- `mypy`
- `flake8`
- `black`
- `isort`
- `pydocstyle`

## Requirements

- Python
- pipenv
- pre-commit
- tox
- Docker
- Commitzen

## Resources

This is heavily inspired by: <https://www.youtube.com/watch?v=DhUpxWjOhME>.
