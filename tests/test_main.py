"""Test for project."""

import math

import pytest

from optom_tools import VisualAcuity


@pytest.mark.parametrize(
    "test_input,expected",
    [
        pytest.param("6/6", math.log10(6 / 6), id="6/6"),
        pytest.param("6 / 6", math.log10(6 / 6), id="6/6 with spaces"),
        pytest.param("6 /120", math.log10(6 / 120), id="6/120 with spaces"),
    ],
)
def test_visual_acuity_to_logmar(test_input, expected):
    """Test visual acuity conversion to logmar."""
    visual_acuity = VisualAcuity(test_input)
    assert visual_acuity.logmar == expected
