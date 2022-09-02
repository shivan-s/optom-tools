"""Testing clean output functions."""

import pytest

from optom_tools.utils import strip_decimal


class TestCleanOutput:
    """Test clean_output functions."""

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            pytest.param((1.122, None), "1.1", id="3 decimal places"),
            pytest.param((1.0, None), "1", id="1 decimal place"),
            pytest.param((1, None), "1", id="no decimal places"),
            pytest.param((1.122, 2), "1.12", id="3 decimal places, return 2"),
        ],
    )
    def test_strip_decimal(self, test_input, expected):
        """Test strip decimal."""
        if test_input[1] is not None:
            assert strip_decimal(test_input[0], test_input[1]) == expected
        else:
            assert strip_decimal(test_input[0]) == expected
