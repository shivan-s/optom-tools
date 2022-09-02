"""Supporting models for the `VisualAcuity` model."""

from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    """Monkey patching pydantic `BaseModel`."""

    class Config:
        """Configation of model."""

        validate_assignment = True
