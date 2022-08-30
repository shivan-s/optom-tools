# Optom Tools

`optom-tools` are a set of tools for working with data associated in the wonderful world of optometry.

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

>>> print(str(prescription))
"-1.00 / +2.00 x 90"
```

## Prescription

::: optom_tools.Prescription
    options:
      members:
        - transpose
        - rx
      show_source: false



## Visual Acuity

*Work in progress*

<!-- ::: optom_tools.VisualAcuity -->
<!--     options: -->
<!--       show_source: false -->
