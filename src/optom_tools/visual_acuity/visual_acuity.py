"""Main Visual Acuity class for module."""

import math
from decimal import Decimal
from typing import Optional, Tuple

import pydantic
from typing_extensions import Literal

from optom_tools.utils import strip_decimal

from .exceptions import VisualAcuityError
from .models import BaseModel

D = Decimal

FT_M = 0.3048  # 1 ft = 0.3048 m


class VisualAcuity(BaseModel):
    """The `visual_acuity` module contains methods in handling visual acuity measurements.

    Input for this class can be provided as keyword arguments. However, a string \
    such as '6/6' can be parsed as well.

    Args:
        numerator (int): The test distance.
        denominator (int): This distance required to subtend 5 minutes of arc.
        unit (Literal["ft", "m"]): Takes feet or metres/meters only. Defaults to 'm', but please check examples for nuances.

    Examples:
        Typical use:
        >>> va = VisualAcuity(numerator=6, denominator=6)
        >>> str(va)
        '6/6'

        If you want to explicitly mention the units:
        >>> va_feet = VisualAcuity(numerator=20, numerator=20, unit="ft")
        >>> str(va_feet)
        '20/20'

        Parsing more familiar input:
        >>> va_familiar = VisualAcuity('6/120')
        >>> va_familiar
        VisualAcuity(numerator=6.0, denominator=120.0, unit='m')

        If the numerator is greater `6`, then the unit is assumed to be feet.
        >>> va_familiar_ft = VisualAcuity('20/200')
        >>> va_familiar_ft
        VisualAcuity(numerator=20.0, denominator=200.0, unit='ft')
    """

    numerator: float = 6
    denominator: float = 6
    unit: Literal["ft", "m"] = "m"

    @pydantic.validator("numerator")
    @classmethod
    def _numerator_validator(cls, value):
        """Validate distance.

        Numerator must be a positive number.
        """
        if value < 0:
            raise VisualAcuityError(
                value=value, message="Distance must be a positive value"
            )
        return value

    @pydantic.validator("denominator")
    @classmethod
    def _denominator_validator(cls, value):
        """Validate denominator.

        Denominator must be a positive number.
        """
        if value < 0:
            raise VisualAcuityError(
                value=value, message="Distance must be a positive value"
            )
        return value

    def __init__(self, *args, **kwargs):
        """Init method."""
        if len(args) >= 1:
            components = self._simple_parse_va(args[0])
            kwargs["numerator"] = components[0]
            kwargs["denominator"] = components[1]
            kwargs["unit"] = components[2]
        super().__init__(**kwargs)

    def _convert_ft_m(self, ft: float) -> float:
        """Convert feet into metres/meters."""
        return round(ft * FT_M)

    def _convert_m_ft(self, m: float) -> float:
        """Convert meters/metres into feet."""
        return round(m / FT_M)

    def convert_unit(self, flag: Optional[Literal["ft", "m"]] = None) -> None:
        """Convert the unit of visual acuity between feet and metres.

        Args:
            flag (Optional[Literal["ft", "m"]]): Flag to ensure a conversion to a particular unit.

        Raises:
            VisualAcuityError: Only accepts `'ft'` and `'m'`as options.

        Examples:
            Converting without a flag:
            >>> va = VisualAcuity(numerator=6, denominator=6)
            >>> va.unit
            'm'
            >>> va.convert_unit()
            >>> str(va)
            '20/20'
            >>> va.unit
            'ft'

            Converting with an 'ft' flag:
            >>> va = VisualAcuity(numerator=20, denominator=20, unit="ft")
            >>> va.convert_unit("ft")
            >>> str(va)
            '20/20'
        """
        if flag not in ["ft", "m"]:
            raise VisualAcuityError(
                value=flag,
                message="Method convert_unit() only accepts flags 'ft' and 'm'",
            )
        if flag != self.unit:
            if self.unit == "ft":
                self.numerator = self._convert_ft_m(self.numerator)
                self.denominator = self._convert_ft_m(self.denominator)
                self.unit = "m"
            elif self.unit == "m":
                self.numerator = self._convert_m_ft(self.numerator)
                self.denominator = self._convert_m_ft(self.denominator)
                self.unit = "ft"

    @property
    def ft(self) -> str:
        """Return snellen fraction representation in feet.

        Returns:
            (str): Snellen Fraction in feet.

        Examples:
            Typical use:
            >>> va = VisualAcuity('6/6')
            >>> va.ft
            '20/20'
        """
        numerator = self.numerator
        denominator = self.denominator
        if self.unit != "ft":
            numerator = self._convert_m_ft(self.numerator)
            denominator = self._convert_m_ft(self.denominator)
        return f"{strip_decimal(numerator)}/{strip_decimal(denominator)}"

    @property
    def m(self) -> str:
        """Return snellen fraction in metres/meters.

        Returns:
            str: Snellen Fraction in meters/metres.

        Examples:
            Typical use:
            >>> va = VisualAcuity('20/20')
            >>> va.m
            '6/6'
        """
        numerator = self.numerator
        denominator = self.denominator
        if self.unit != "m":
            numerator = self._convert_ft_m(self.numerator)
            denominator = self._convert_ft_m(self.denominator)
        return f"{strip_decimal(numerator)}/{strip_decimal(denominator)}"

    @property
    def snellen_fraction(self) -> str:
        """Return snellen fraction representation of visual acuity.

        Returns:
            str: snellen fraction.

        Examples:
            Typical use:
            >>> VisualAcuity("6 / 12").snellen_fraction
            "6/6"
        """
        return f"{strip_decimal(self.numerator)}/{strip_decimal(self.denominator)}"

    @property
    def decimal(self) -> Decimal:
        """Return decimal form of visual acuity.

        Returns:
            Decimal: Decimal form of visual acuity.

        Examples:
            Typical use:
            >>> VisualAcuity("6/12").decimal
            0.5
        """
        return D(self.numerator / self.denominator)

    @property
    def logmar(self) -> Decimal:
        """Return logmar value of the visual acuity.

        Returns:
            Decimal: Logmar value of the visual acuity.

        Examples:
            Typical use:
            >>> VisualAcuity("6/6").logmar
            0.0
        """
        return D(math.log10(self.decimal))

    def _simple_parse_va(self, va: str) -> Tuple[str, str, Literal["ft", "m"]]:
        """Parse va string into a tuple.

        This tuple is numerator, denominator, unit.
        """
        components = va.split("/")
        if len(components) != 2:
            raise VisualAcuityError(
                value=va,
                message="Input must contain one '/' and numbers (e.g. '6/6')",
            )
        numerator = components[0]
        denominator = components[1]
        unit: Literal["ft", "m"] = "m"
        if numerator == "":
            numerator = "6"
        if float(numerator) > 6:
            unit = "ft"
        return (numerator, denominator, unit)

    def parse(self, va: str) -> BaseModel:
        """Parse a string into a visual acuity.

        Note: if the test distance (numerator) is greater than 6, then the unit is assumed to be in feet.

        Args:
            va (str): A visual acuity.

        Examples:
            Parsing a visual acuity:
            >>> va = VisualAcuity().parse('6/120')
            >>> str(va)
            '6/120'
            Parsing a visual acuity, automatically turning into a feet:
            >>> va = VisualAcuity().parse('20/20')
            >>> va.unit
            'ft'
        """
        components = self._simple_parse_va(va=va)
        self.numerator = float(components[0])
        self.denominator = float(components[1])
        self.unit = components[2]

        if self.numerator > 6:
            self.unit = "ft"

        return self

    def __str__(self) -> str:
        """Give string representation."""
        return self.snellen_fraction
