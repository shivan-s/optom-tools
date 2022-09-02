"""Supporting models for the main Prescription model."""

from typing import Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import validator
from typing_extensions import Literal

from .exceptions import PrescriptionError


class BaseModel(PydanticBaseModel):
    """Monkey patching pydantic `BaseModel`."""

    class Config:
        """Configation of model."""

        validate_assignment = True


class BasePrism(BaseModel):
    """Base Prism model."""

    magnitude: float = 0

    @validator("magnitude", allow_reuse=True)
    @classmethod
    def _magnitude_validate(cls, value: float) -> float:
        """Validate magnitude.

        The magnitude of a prism must be positive.
        """
        if value < 0:
            raise PrescriptionError(
                value=value,
                message="The prism dioptre must be a positive number",
            )
        return value


class HorizontalPrism(BasePrism):
    """Horizontal Prism model.

    Note that the direction is related to base direction (e.g. right, left, in
    out).
    """

    direction: Optional[Literal["R", "L", "I", "O"]] = None


class VerticalPrism(BasePrism):
    """Vertical Prism model.

    Note that the direction is related to base direction (e.g. up, down).
    """

    direction: Optional[Literal["U", "D"]] = None


class Add(BaseModel):
    """Add model.

    A patient's add along with working distance (e.g. +2.00 @ 40cm for music).
    """

    add: float = 0.0
    working_distance_cm: float = 40
    description: str = ""

    @validator("add")
    @classmethod
    def _add_validate(cls, value: float) -> float:
        """Validate add.

        Add must be a positive number.
        """
        if value < 0:
            raise PrescriptionError(
                value=value, message="Add must be a positive number"
            )
        return value

    @validator("working_distance_cm")
    @classmethod
    def _working_distance_cm_validate(cls, value: float) -> float:
        """Validate add.

        The working distance must be positive and no more than 600cm (what is considered optical infinity).
        """
        if value < 0 or value > 600:
            raise PrescriptionError(
                value=value,
                message="Working Distance (cm) must be greater than 0 cm and no greater than 600cm",
            )
        return value
