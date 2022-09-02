"""Tests for visual_acuity module."""

import math
from contextlib import nullcontext as does_not_raise
from decimal import Decimal

import pytest

from optom_tools import VisualAcuity
from optom_tools.visual_acuity.exceptions import VisualAcuityError


class TestVisualAcuity:
    """Testing methods and attritbutes for `VisualAcuity`."""

    @pytest.mark.parametrize(
        "test_input,expected,exception,exception_message",
        [
            pytest.param(
                {"numerator": 6, "denominator": 6},
                "6/6",
                does_not_raise(),
                None,
                id="6/6",
            ),
            pytest.param(
                {"numerator": 6, "denominator": -6},
                None,
                pytest.raises(VisualAcuityError),
                "Distance must be a positive value",
                id="ERROR negative denominator",
            ),
            pytest.param(
                {"numerator": -6, "denominator": 6},
                None,
                pytest.raises(VisualAcuityError),
                "Distance must be a positive value",
                id="ERROR negative numerator",
            ),
        ],
    )
    def test_initialising_object(
        self, test_input, expected, exception, exception_message
    ):
        """Test VisualAcuity initialisation."""
        with exception as excinfo:
            va = VisualAcuity(**test_input)
            assert str(va) == expected
        if excinfo is not None:
            assert excinfo.value.message == exception_message

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            pytest.param(
                VisualAcuity(numerator=6, denominator=6, unit="m"),
                "20/20",
                id="6/6",
            ),
            pytest.param(
                VisualAcuity(numerator=6, denominator=3, unit="m"),
                "20/10",
                id="6/6",
            ),
            pytest.param(
                VisualAcuity(numerator=20, denominator=20, unit="ft"),
                "20/20",
                id="20/20",
            ),
        ],
    )
    def test_ft(self, test_input, expected):
        """Test VisualAcuity initialisation."""
        assert test_input.ft == expected

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            pytest.param(
                VisualAcuity(numerator=6, denominator=6, unit="m"),
                "6/6",
                id="6/6",
            ),
            pytest.param(
                VisualAcuity(numerator=20, denominator=20, unit="ft"),
                "6/6",
                id="20/20",
            ),
            pytest.param(
                VisualAcuity(numerator=20, denominator=10, unit="ft"),
                "6/3",
                id="20/20",
            ),
        ],
    )
    def test_m(self, test_input, expected):
        """Test VisualAcuity initialisation."""
        assert test_input.m == expected

    @pytest.mark.parametrize(
        "test_input,test_flag,expected,exception,exception_message",
        [
            pytest.param(
                VisualAcuity(numerator=6, denominator=6, unit="m"),
                "ft",
                VisualAcuity(numerator=20, denominator=20, unit="ft"),
                does_not_raise(),
                None,
                id="m to ft",
            ),
            pytest.param(
                VisualAcuity(numerator=20, denominator=20, unit="ft"),
                "m",
                VisualAcuity(numerator=6, denominator=6, unit="m"),
                does_not_raise(),
                None,
                id="ft to m",
            ),
            pytest.param(
                VisualAcuity(numerator=20, denominator=10, unit="ft"),
                "wrong flag",
                VisualAcuity(numerator=20, denominator=10, unit="ft"),
                pytest.raises(VisualAcuityError),
                "Method convert_unit() only accepts flags 'ft' and 'm'",
                id="ERROR wrong flag",
            ),
        ],
    )
    def test_convert_unit(
        self, test_input, test_flag, expected, exception, exception_message
    ):
        """Test VisualAcuity initialisation."""
        with exception as excinfo:
            if test_flag is not None:
                test_input.convert_unit(test_flag)
            else:
                test_input.convert_unit()
            assert test_input == expected
        if excinfo is not None:
            assert excinfo.value.message == exception_message

    @pytest.mark.parametrize(
        "test_input,expected,exception,exception_message",
        [
            pytest.param(
                "6/6",
                VisualAcuity(numerator=6, denominator=6),
                does_not_raise(),
                None,
                id="6/6",
            ),
            pytest.param(
                "20/200",
                VisualAcuity(numerator=20, denominator=200, unit="ft"),
                does_not_raise(),
                None,
                id="20/200",
            ),
            pytest.param(
                "20/200/",
                VisualAcuity(numerator=20, denominator=200, unit="ft"),
                pytest.raises(VisualAcuityError),
                "Input must contain one '/' and numbers (e.g. '6/6')",
                id="ERROR Too many '/'",
            ),
            pytest.param(
                "/5",
                VisualAcuity(numerator=6, denominator=5),
                does_not_raise(),
                None,
                id="/5",
            ),
        ],
    )
    def test_parse(self, test_input, expected, exception, exception_message):
        """Test parsing of string into visual acuity."""
        with exception as excinfo:
            va_parse = VisualAcuity(test_input)
            assert va_parse == expected
        if excinfo is not None:
            assert excinfo.value.message == exception_message

        with exception as excinfo:
            va_parse = VisualAcuity().parse(test_input)
            assert va_parse == expected
        if excinfo is not None:
            assert excinfo.value.message == exception_message

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            pytest.param(
                {"numerator": 6, "denominator": 6},
                Decimal(math.log10(6 / 6)),
                id="6/6",
            ),
            pytest.param(
                {"numerator": 6, "denominator": 120},
                Decimal(math.log10(6 / 120)),
                id="6/120",
            ),
        ],
    )
    def test_visual_acuity_to_logmar(self, test_input, expected):
        """Test visual acuity conversion to logmar."""
        va = VisualAcuity(**test_input)
        assert va.logmar == expected
