"""Pydantic models for the visual acuity module."""

from typing import Literal

from pydantic import BaseModel


class Va(BaseModel):
    """Visual Acuity model."""

    numerator: float
    denominator: float
    unit: Literal["ft", "m"] = "m"
