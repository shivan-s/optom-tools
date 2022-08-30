# Optom Tools

[![Build](https://github.com/shivan-s/optom-tools/actions/workflows/build.yml/badge.svg)](https://github.com/shivan-s/python-template/actions/workflows/build.yml)
[![pages-build-deployment](https://github.com/optom-tools/python-template/actions/workflows/pages/pages-build-deployment/badge.svg?branch=gh-pages)](https://github.com/shivan-s/python-template/actions/workflows/pages/pages-build-deployment)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)

## ⚠️ Under develepment ⚠️

## Getting Started

Install with `pip` or your other favourite package manager (e.g. `pipenv` or `poetry`).

```shell
pip install optom-tools
```

## Simple Example

```python
>>> from optom_tools import Prescription

>>> prescription = Prescription("+1.00/-2.00x180")

>>> prescription.transpose()

>>> prescription

"-1.00 / +2.00 x 90"
```

## Docs

Comprehensive documentation can be found here: <https://shivan-s.github.io/optom-tools>

## Contribution

Yes, please.
