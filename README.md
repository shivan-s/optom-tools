# Optom Tools ⚠️ Under develepment ⚠️

[![Build](https://github.com/shivan-s/optom-tools/actions/workflows/build.yml/badge.svg)](https://github.com/shivan-s/optom-tools/actions/workflows/build.yml)
[![Deploy Docs](https://github.com/shivan-s/optom-tools/actions/workflows/docs.yml/badge.svg)](https://github.com/shivan-s/optom-tools/actions/workflows/docs.yml)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
[![Latest Version](https://img.shields.io/pypi/v/optom-tools.svg)](https://pypi.python.org/pypi/optom-tools/)
[![Format](https://img.shields.io/pypi/format/optom-tools.svg)](https://pypi.python.org/pypi/optom-tools/)
[![Python Versions](https://img.shields.io/pypi/pyversions/optom-tools.svg)](https://pypi.python.org/pypi/optom-tools/)
[![Implementation](https://img.shields.io/pypi/implementation/optom-tools.svg)](https://pypi.python.org/pypi/optom-tools/)
[![License](https://img.shields.io/pypi/status/optom-tools.svg)](https://pypi.python.org/pypi/optom-tools/)

## Getting Started

Install with `pip` or your other favourite package manager (e.g. `pipenv` or `poetry`).

```shell
pip install optom-tools
```

## Simple Example

```python
>>> from optom_tools import Prescription

>>> prescription = Prescription.parse("+1.00/-2.00x180")

>>> prescription.transpose()

>>> str(prescription)

"-1.00 / +2.00 x 90"
```

## Docs

Comprehensive documentation can be found here: <https://shivan-s.github.io/optom-tools>

## Contribution

Yes, please. I'd love some help on this.
