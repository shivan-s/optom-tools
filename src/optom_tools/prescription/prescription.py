"""Main entry point for the pydantic model."""

from typing import List, Optional

import pydantic
from typing_extensions import Literal

from optom_tools.utils import strip_decimal

from .exceptions import PrescriptionError
from .models import Add, BaseModel, HorizontalPrism, VerticalPrism


class Prescription(BaseModel):
    """The prescription module contains methods to deal with spectacle prescriptions.

    Examples:
        Typical use:
        >>> rx = Prescription(sphere=0, cylinder=-1, axis=180)
        >>> str(rx)
        'plano / -1.00 x 180'
    """

    sphere: float = 0
    cylinder: float = 0
    axis: float = 180
    add: Add = Add()
    intermediate_add: Add = Add(working_distance_cm=50)
    back_vertex_mm: float = 12.0

    vertical_prism: VerticalPrism = VerticalPrism()
    horizontal_prism: HorizontalPrism = HorizontalPrism()
    reading_vertical_prism: VerticalPrism = VerticalPrism()
    reading_horizontal_prism: HorizontalPrism = HorizontalPrism()
    extra_adds: List[Add] = []

    @pydantic.validator("axis")
    @classmethod
    def _axis_valid(cls, value: float) -> float:
        """Validate axis.

        Axis must be between 180 to 0 degrees.
        """
        if value > 180 or value < 0:
            raise PrescriptionError(
                value=value, message="Axis must be between 0 and 180 degrees"
            )
        return value

    @property
    def mean_sphere(self) -> float:
        """Provide mean sphere value of the prescription.

        Returns:
            (float): The Mean Sphere.
        """
        return self.sphere + (self.cylinder / 2)

    def transpose(self, flag: Optional[Literal["n", "p"]] = None) -> None:
        """Transpose prescription from positive to negative and vice versa.

        Flags, `'n'` and `'p'`, can be provided to force a negative or positive cylinder respectively.

        Args:
            (Optional[[Literal["n", "p"]]): Flag to force negative ('n') and positive ('p') cylindrical format. Defaults to `None`.

        Examples:
            Transposing a prescription as normal:
            >>> rx = Prescription("+1.00/-1.00x180")
            >>> rx.transpose()
            >>> str(rx)
            "plano / +1.00 x 90"
            >>> rx.transpose()
            >>> str(rx)
            "+1.00 / -1.00 x 180"

            Transposing a prescription with the 'n' flag:
            >>> rx = Prescription("+1.00/-1.00x180").transpose('n')
            >>> str(rx)
            "+1.00 / -1.00 x 180"
        """
        if flag is not None and flag not in ["n", "p"]:
            raise PrescriptionError(
                value=flag,
                message="Method transpose() only accepts 'n' and 'p' as input flags",
            )
        if (
            flag == "n"
            and self.cylinder > 0
            or flag == "p"
            and self.cylinder < 0
            or flag is None
            and self.cylinder != 0
        ):
            self.sphere = self.sphere + self.cylinder
            self.cylinder = -1 * self.cylinder
            new_axis = self.axis + 90
            if new_axis > 180:
                new_axis = new_axis - 180
            self.axis = new_axis

    def _simple_parse_rx(self, rx: str) -> None:
        """Parse rx for a simple input.

        For example: simple input is '+1.00/-1.00x90'
        """
        # TODO: parse this '+1.00/-1.00x90 Add +2.00@40'
        rx_components = rx.split("/")
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

        self.sphere = float(sphere)
        self.cylinder = float(cylinder)
        self.axis = float(axis)

    def parse(self, rx: str, efficient_parser: bool = False) -> BaseModel:
        """Parse a prescription in a more typical format.

        This is more familiar than setting a prescription using keyword arguments.

        Args:
            rx (str): The prescription as a string.
            efficient_parser (bool): If set to `True`, will use the efficient parser as opposed to simple.

        Examples:
            Parsing a simple prescription:
            >>> rx = Prescription().parse("+1.00/-1.00x180")
            >>> rx.transpose()
            >>> str(rx)
            'pl / +1.00 x 90'

            Parsing a 'efficient' prescription:
            >>> # TODO!
            >>> # Coming soon.
        """
        if not efficient_parser:
            self._simple_parse_rx(rx)
        return self
        # TODO: efficient Rx parser to be written.

    def __str__(self) -> str:
        """Provide string representation of object."""

        def _give_plus_sign(value: float) -> str:
            """Will append '+' if the value is positive and will return value to 2 decimal places."""
            if value >= 0:
                return f"+{value:0.2f}"
            else:
                return f"{value:0.2f}"

        str_lst = []
        if self.sphere == 0:
            str_lst.append("plano")
        else:
            str_lst.append(_give_plus_sign(self.sphere))

        if self.sphere != 0 and self.cylinder == 0:
            str_lst.append(" DS")
        elif self.cylinder != 0:
            str_lst.append(" / ")
            str_lst.append(_give_plus_sign(self.cylinder))

            str_lst.append(" x ")
            str_lst.append(strip_decimal(self.axis))

        # deal with add

        # intermediate add

        # prisms
        return "".join(str_lst)
