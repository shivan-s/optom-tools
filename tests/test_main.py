"""Test for project."""

import math

import pytest

from optom_tools import Prescription, Rx, VisualAcuity


@pytest.mark.parametrize(
    "input,expected",
    [
        pytest.param("6/6", math.log10(6 / 6), id="6/6"),
        pytest.param("6 / 6", math.log10(6 / 6), id="6/6 with spaces"),
        pytest.param("6 /120", math.log10(6 / 120), id="6/120 with spaces"),
    ],
)
def test_visual_acuity_to_logmar(input, expected):
    """Test visual acuity conversion to logmar."""
    visual_acuity = VisualAcuity(input)
    assert visual_acuity.logmar == expected


class TestPrescription:
    """Prescription testing."""

    @pytest.mark.parametrize(
        "input,expected",
        [
            pytest.param("pl", Rx(sphere=0), id="Plano"),
            pytest.param(
                "plano/-0.75x180",
                Rx(sphere=0, cylinder=-0.75, axis=180),
                id="Cyl",
            ),
            pytest.param("+1.00", Rx(sphere=1.0), id="Sphere only"),
            pytest.param(
                "+1.00/+0.75x180",
                Rx(sphere=1.75, cylinder=-0.75, axis=90),
                id="Positive cyl.",
            ),
        ],
    )
    def test_prescription_negative_cyl(self, input, expected):
        """Prescription negative cyl attribute."""
        rx = Prescription(input)
        assert rx.negative_cyl == expected

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
    def test_prescription_str(self, input, expected):
        """Prescription string representation."""
        rx = Prescription(input)
        assert str(rx) == expected
