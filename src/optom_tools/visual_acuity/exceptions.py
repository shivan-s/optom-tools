"""Custom exceptions related to the `visual_acuity` module."""

from typing import Any


class VisualAcuityError(Exception):
    """Prescription input error."""

    def __init__(self, value: Any, message: str) -> None:
        """Construct exception."""
        self.value = value
        self.message = message
        super().__init__(message)
