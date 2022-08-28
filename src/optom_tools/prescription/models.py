"""Pydantic models related to the prescription module."""

from typing import Literal

from pydantic import BaseModel, validator

from .exceptions import PrescriptionInputError


class BasePrism(BaseModel):
    """Base Prism model."""

    magnitude: float = 0


class HorizontalPrism(BasePrism):
    """Horizontal Prism model.

    Note that the direction is related to base direction (e.g. right, left, in
    out).
    """

    direction: Literal["R", "L", "I", "O"] | None


class VerticalPrism(BasePrism):
    """Vertical Prism model.

    Note that the direction is related to base direction (e.g. up, down).
    """

    direction: Literal["U", "D"] | None


class Add(BaseModel):
    """Add model.

    A patient's add along with working distance (e.g. +2.00 @ 40cm).
    """

    add: float = 0.0
    working_distance_cm: float = 40


class Rx(BaseModel):
    """Rx model.

    This is the models the prescription (rx is shorthand).
    """

    sphere: float = 0
    cylinder: float = 0
    axis: float = 180
    vertical_prism: VerticalPrism = VerticalPrism()
    horizontal_prism: HorizontalPrism = HorizontalPrism()
    add: Add = Add()
    intermediate_add: float = 0
    extra_adds: list[Add] = []
    back_vertex_mm: float = 12.0

    @validator("axis")
    @classmethod
    def axis_valid(cls, value: float) -> float:
        """Validate axis."""
        if value >= 180 and value <= 0:
            raise PrescriptionInputError(
                value=value, message="Axis must be between 0 and 180 degrees"
            )
        return value
