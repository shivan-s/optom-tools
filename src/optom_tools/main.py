"""Main entry point."""

import logging
import math
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, validator
from rich.logging import RichHandler

D = Decimal

FORMAT = "%(message)s"
LEVEL = "DEBUG"
DATEFMT = "[%X]"
logging.basicConfig(
    level=LEVEL, format=FORMAT, datefmt=DATEFMT, handlers=[RichHandler()]
)
log = logging.getLogger("rich")


class PrescriptionInputError(Exception):
    """Exception for axis value."""

    def __init__(self, value: float, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class Va(BaseModel):
    numerator: float
    denominator: float


class BasePrism(BaseModel):
    magnitude: float = 0


class HorizontalPrism(BasePrism):
    direction: Literal["R", "L", "I", "O"] | None


class VerticalPrism(BasePrism):
    direction: Literal["U", "D"] | None


class Rx(BaseModel):
    sphere: float = 0
    cylinder: float = 0
    axis: float = 180
    vertical_prism: VerticalPrism = VerticalPrism()
    horizontal_prism: HorizontalPrism = HorizontalPrism()
    add: float = 0
    intermediate_add: float = 0
    extra_adds: list[float] = []

    @validator("axis")
    @classmethod
    def axis_valid(cls, value: float) -> float:
        """Validate axis."""
        if value >= 180 and value <= 0:
            raise PrescriptionInputError(
                value=value, message="Axis must be between 0 and 180 degrees"
            )
        return value


class OptomTools:
    """Main class."""

    def __init__(self):
        pass


class Prescription:
    """Prescription."""

    def __init__(self, rx: str) -> None:
        self.rx = rx

    def _parse_rx(self) -> Rx:
        rx_components = self.rx.split("/")
        sphere = rx_components[0]
        cylinder = "0"
        axis = "180"
        if len(rx_components) > 1:
            cylinder_all = rx_components[1]

            cyl_components = cylinder_all.split("x")
            cylinder = cyl_components[0]
            axis = cyl_components[1]

        if type(sphere) == str and sphere[0:2] == "pl":
            sphere = "0"

        return Rx(sphere=sphere, cylinder=cylinder, axis=axis)

    def _convert_cyl(self) -> Rx:
        rx = self._parse_rx()
        new_axis = rx.axis + 90
        if new_axis > 180:
            new_axis = new_axis - 180

        return Rx(
            sphere=(rx.sphere + rx.cylinder),
            cylinder=(-1 * rx.cylinder),
            axis=new_axis,
        )

    @property
    def postive_cyl(self):
        rx = self._parse_rx()
        if rx.cylinder < 0:
            return self._convert_cyl()
        return rx

    @property
    def negative_cyl(self):
        rx = self._parse_rx()
        if rx.cylinder > 0:
            return self._convert_cyl()
        return rx

    def __str__(self) -> str:
        rx = self._parse_rx()

        str_lst = []
        if rx.sphere > 0:
            str_lst.append("+")

        if rx.sphere == 0:
            str_lst.append("plano")
        else:
            str_lst.append(f"{rx.sphere:0.2f}")

        if rx.sphere != 0 and rx.cylinder == 0:
            str_lst.append(" DS")
        elif rx.cylinder != 0:
            str_lst.append(" / ")
            str_lst.append(f"{rx.cylinder:0.2f}")
            str_lst.append(" x ")
            str_lst.append(f"{rx.axis}")
        return "".join(str_lst)


class VisualAcuity:
    """Visual Acuity."""

    def __init__(
        self,
        acuity: str,
        unit: Literal["m", "metre", "metres", "ft", "feet"] = "m",
    ) -> None:
        """Construct VisualAcuity class.

        Args:
            acuity (str): The visual acuity (e.g. 6/6)
        """
        self.acuity = acuity
        self.unit = unit

    def _parse_acuity(self) -> Va:
        acuity = self.acuity.split("/")
        return Va(numerator=acuity[0], denominator=acuity[1])

    @property
    def snellen_fraction(self) -> str:
        acuity = self._parse_acuity()
        return f"{acuity.numerator/acuity.denominator}"

    @property
    def decimal(self) -> Decimal:
        """Return decimal form of visual acuity.

        Returns:
            [TODO:return]
        """
        acuity = self._parse_acuity()
        return D(acuity.numerator / acuity.denominator)

    @property
    def logmar(self) -> Decimal:
        return D(math.log10(self.decimal))

    def __str__(self) -> str:
        return self.snellen_fraction

    def __repr__(self) -> str:
        acuity = self._parse_acuity()
        return f"{__class__}(numerator={acuity.numerator}, denominator={acuity.denominator})"
