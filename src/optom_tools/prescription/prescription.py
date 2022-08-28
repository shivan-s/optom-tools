"""Prescription."""

from typing import Literal

from .exceptions import PrescriptionInputError, TransposeInputError
from .models import Rx

# Efficient Rx -> Real Rx
# "0\n4" -> R plano
#           L +1.00 DS
# "4#" -> R +1.00 DS
#         L +1.00 DS
# "4.-4#110\nx90" -> R +1.00/-1.00x110
#                    L plano/-1.00x90
# "12#.-8#x180#.12# -> R +3.00/-2.00x180  Add: +3.00
#                      L +3.00/-2.00x180  Add: +3.00
# "27.-5x35.6\n30.-11x85.8" -> R +6.75/-1.25x35 Add: +1.50
#                              L +7.50/-2.75x85 Add: +2.00
# "4.8i12u\n30.12.-3x70.8i.8d" -> R +1.00 DS 2 In 3 Up
#                                 L +3.00/-0.75x70 2 In 2 Down
# "0#.6#" -> R plano Add: +1.50
#            L plano Add: +1.50


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
