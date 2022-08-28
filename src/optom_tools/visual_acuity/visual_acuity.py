"""Main Visual Acuity class for module."""

import math
from decimal import Decimal
from typing import Literal

from .models import Va

D = Decimal


class VisualAcuity:
    """Visual Acuity."""

    def __init__(
        self,
        acuity: str,
        unit: Literal["m", "metre", "metres", "ft", "feet"] = "m",
    ) -> None:
        """Construct VisualAcuity class.

        Args:
            acuity (str): The visual acuity (e.g. 6/6).
            unit (Literal["m", "metre", "metres", "ft", "feet"]): Unit of
            visual acuity.
        """
        self._acuity = acuity
        self._unit = unit

    def _parse_acuity(self) -> Va:
        acuity = self._acuity.split("/")
        return Va(numerator=acuity[0], denominator=acuity[1])

    @property
    def snellen_fraction(self) -> str:
        """Return snellen fraction representation of visual acuity.

        Returns:
            str: snellen fraction.

        Examples:
            >>> VisualAcuity("6 / 6").snellen_fraction
            "6/6"

        """
        acuity = self._parse_acuity()
        return f"{acuity.numerator/acuity.denominator}"

    @property
    def decimal(self) -> Decimal:
        """Return decimal form of visual acuity.

        Returns:
            (Decimal): Decimal form of visual acuity.

        Examples:
        >>> VisualAcuity("6/6").decimal
        1.0
        """
        acuity = self._parse_acuity()
        return D(acuity.numerator / acuity.denominator)

    @property
    def logmar(self) -> Decimal:
        """Return logmar value of the visual acuity.

        Returns:
            (Decimal): Logmar value of the visual acuity.

        Examples:
        >>> VisualAcuity("6/6").logmar
        0.0
        """
        return D(math.log10(self.decimal))

    def __str__(self) -> str:
        """Give string representation."""
        return self.snellen_fraction
