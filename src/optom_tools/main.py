"""Main entry point for optom_tools."""

import logging
from decimal import Decimal

from rich.logging import RichHandler

from .prescription import Prescription
from .visual_acuity import VisualAcuity

__all__ = ["Prescription", "VisualAcuity"]

D = Decimal

FORMAT = "%(message)s"
LEVEL = "DEBUG"
DATEFMT = "[%X]"
logging.basicConfig(
    level=LEVEL, format=FORMAT, datefmt=DATEFMT, handlers=[RichHandler()]
)
log = logging.getLogger("rich")


def main():
    """Entry function."""
    pass


if __name__ == "__main__":
    main()
