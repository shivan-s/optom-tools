"""Testing for prescription."""

import pytest

from optom_tools import Prescription
from optom_tools.prescription.models import Rx


class TestPrescription:
    """Prescription testing."""

    @pytest.mark.parametrize(
        "input,value,expected",
        [
            pytest.param("pl", None, Rx(sphere=0), id="Plano/Sphere only"),
            pytest.param(
                "plano/-0.75x180",
                None,
                Rx(sphere=-0.75, cylinder=+0.75, axis=90),
                id="no transpose flag",
            ),
            pytest.param(
                "+1.00/-0.75x180",
                "n",
                Rx(sphere=1.00, cylinder=-0.75, axis=180),
                id="n flag",
            ),
            pytest.param(
                "+1.00/-0.75x180",
                "p",
                Rx(sphere=0.25, cylinder=0.75, axis=90),
                id="p flag",
            ),
            pytest.param(
                "+1.00/+0.75x180",
                None,
                Rx(sphere=1.75, cylinder=-0.75, axis=90),
                id="positive cyl, no flag",
            ),
        ],
    )
    def test_prescription_transpose_rx(self, input, value, expected):
        """Prescription negative cyl attribute."""
        test_rx = Prescription(input)
        if value is None:
            test_rx.transpose()
        else:
            test_rx.transpose(value)
        assert test_rx.rx.sphere == expected.sphere
        assert test_rx.rx.cylinder == expected.cylinder
        assert test_rx.rx.axis == expected.axis

    @pytest.mark.parametrize(
        "input,expected",
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
        "input,expected",
        [
            pytest.param("pl", Rx(sphere=0), id="Plano"),
            pytest.param(
                "plano/-0.75x180",
                Rx(sphere=0, cylinder=-0.75, axis=180),
                id="Cyl",
            ),
        ],
    )
    def test_prescription_repr(self, test_input, expected):
        """Prescrption representation."""
        rx = Prescription(test_input)
        assert rx == expected
