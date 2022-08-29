"""Prescription."""

from typing import Literal

from .exceptions import PrescriptionInputError, TransposeInputError
from .models import Rx


class Prescription:
    """Prescription."""

    def __init__(
        self,
        rx: str,
        rx_type: Literal["simple", "efficient"] | None = "simple",
    ) -> None:
        """Construct prescription."""
        self._rx = rx
        self._rx_type = rx_type

        if self._rx_type not in ["simple", "efficient"]:
            raise PrescriptionInputError(
                value=rx_type,
                message="rx_type must be 'simple' or 'efficient'",
            )
        if self._rx_type == "simple":
            self._simple_parse_rx()

    def _simple_parse_rx(self) -> None:
        """Parse input."""
        rx_components = self._rx.split("/")
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

        self._Rx = Rx(sphere=sphere, cylinder=cylinder, axis=axis)

    def _convert_cyl(self) -> None:
        """Change the from negative to positive cylinder and vice versa."""
        rx = self._Rx
        new_axis = rx.axis + 90
        if new_axis > 180:
            new_axis = new_axis - 180

        self._Rx = Rx(
            sphere=(rx.sphere + rx.cylinder),
            cylinder=(-1 * rx.cylinder),
            axis=new_axis,
        )

    @property
    def rx(self) -> Rx:
        """Return prescription."""
        return self._Rx

    def transpose(self, value: Literal["n", "p"] | None = None) -> None:
        """Transpose prescription from positive to negative and vice versa.

        Args:
            value (Literal["n", "p"] | None): Flag to force negative ('n') and
            positive ('p') cylindrical format.
        """
        if value is not None and value not in ["n", "p"]:
            raise TransposeInputError(
                value=value, message="Only accepts 'n' and 'p' as input flags"
            )
        if (
            value == "n"
            and self._Rx.cylinder > 0
            or value == "p"
            and self._Rx.cylinder < 0
            or value is None
            and self._Rx.cylinder != 0
        ):
            self._convert_cyl()

    def __str__(self) -> str:
        """Provide string representation of object."""
        rx = self._Rx

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

    def __repr__(self) -> Rx:
        """Provide representation."""
        return self._Rx
