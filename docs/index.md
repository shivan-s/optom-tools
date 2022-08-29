# Optom Tools

Welcome. These are a set of tools for optometrists.

## Installation

Install with `pip` or your other favourite package manager (e.g. `pipenv` or `poetry`).

```shell
pip install optom-tools
```

## Example

```python
>>> from optom_tools import Prescription

>>> prescription = Prescription("+1.00/-2.00x180")

>>> prescription.transpose()

>>> print(str(prescription))
"-1.00/+2.00x90"
```

## prescription

## Visual Acuity
