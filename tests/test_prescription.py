"""Testing for prescription."""

from contextlib import nullcontext as does_not_raise

import pytest

from optom_tools import Prescription
from optom_tools.prescription.exceptions import (
    PrescriptionInputError,
    TransposeInputError,
)
from optom_tools.prescription.models import Rx


class TestPrescription:
    """Prescription testing."""

    @pytest.mark.parametrize(
        "test_input,expected,exception,exception_message",
        [
            pytest.param(
                "pl",
                Rx(sphere=0),
                does_not_raise(),
                "",
                id="Plano/Sphere only",
            ),
            pytest.param(
                "+1.00/-0.75x180",
                Rx(sphere=1.00, cylinder=-0.75, axis=180),
                does_not_raise(),
                "",
                id="Full Rx",
            ),
            pytest.param(
                "+1.00/-1.00x190",
                None,
                pytest.raises(PrescriptionInputError),
                "Axis must be between 0 and 180 degrees",
                id="Axis out of range",
            ),
        ],
    )
    def test_prescription_parse_simple_rx(
        self, test_input, expected, exception, exception_message
    ):
        """Prescription negative cyl attribute."""
        with exception as excinfo:
            test_rx = Prescription(test_input)
            assert test_rx.rx.sphere == expected.sphere
            assert test_rx.rx.cylinder == expected.cylinder
            assert test_rx.rx.axis == expected.axis
        if excinfo is not None:
            assert excinfo.value.message == exception_message

    @pytest.mark.parametrize(
        "test_input,value,expected,exception",
        [
            pytest.param(
                "pl",
                None,
                Rx(sphere=0),
                does_not_raise(),
                id="Plano/Sphere only",
            ),
            pytest.param(
                "plano/-0.75x180",
                None,
                Rx(sphere=-0.75, cylinder=+0.75, axis=90),
                does_not_raise(),
                id="no transpose flag",
            ),
            pytest.param(
                "+1.00/-0.75x180",
                "n",
                Rx(sphere=1.00, cylinder=-0.75, axis=180),
                does_not_raise(),
                id="n flag",
            ),
            pytest.param(
                "+1.00/-0.75x180",
                "p",
                Rx(sphere=0.25, cylinder=0.75, axis=90),
                does_not_raise(),
                id="p flag",
            ),
            pytest.param(
                "+1.00/+0.75x180",
                None,
                Rx(sphere=1.75, cylinder=-0.75, axis=90),
                does_not_raise(),
                id="positive cyl, no flag",
            ),
            pytest.param(
                "+1.00/+0.75x180",
                "wrong",
                Rx(sphere=1.75, cylinder=-0.75, axis=90),
                pytest.raises(TransposeInputError),
                id="positive cyl, no flag",
            ),
        ],
    )
    def test_prescription_transpose_rx(self, test_input, value, exception, expected):
        """Prescription negative cyl attribute."""
        with exception:
            test_rx = Prescription(test_input)
            if value is None:
                test_rx.transpose()
            else:
                test_rx.transpose(value)
            assert test_rx.rx.sphere == expected.sphere
            assert test_rx.rx.cylinder == expected.cylinder
            assert test_rx.rx.axis == expected.axis

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            pytest.param("pl", "plano", id="Plano"),
            pytest.param(
                "plano/-0.75x180",
                "plano / -0.75 x 180.0",
                id="Cyl",
            ),
            pytest.param("+1.00", "+1.00 DS", id="Sphere only"),
        ],
    )
    def test_prescription_str(self, test_input, expected):
        """Prescription string representation."""
        rx = Prescription(test_input)
        assert str(rx) == expected

    @pytest.mark.parametrize(
        "test_input",
        [
            pytest.param("pl", id="Plano"),
            pytest.param(
                "plano/-0.75x180",
                id="Cyl",
            ),
        ],
    )
    def test_prescription_repr(self, test_input):
        """Prescrption representation."""
        rx = Prescription(test_input)
        assert isinstance(rx, Prescription)
