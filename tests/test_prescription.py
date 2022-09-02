"""Testing for prescription."""

from contextlib import nullcontext as does_not_raise

import pytest

from optom_tools import Prescription
from optom_tools.prescription.exceptions import PrescriptionError


class TestPrescription:
    """Prescription testing."""

    @pytest.mark.parametrize(
        "test_input,expected,exception,exception_message",
        [
            pytest.param({}, "plano", does_not_raise(), None, id="No inputs"),
            pytest.param(
                {"sphere": 1.5, "cylinder": -1, "axis": 90},
                "+1.50 / -1.00 x 90",
                does_not_raise(),
                None,
                id="Normal input",
            ),
            pytest.param(
                {"sphere": 1.5, "cylinder": -1, "axis": 90.5},
                "+1.50 / -1.00 x 90.5",
                does_not_raise(),
                None,
                id="Normal input axis decimal",
            ),
            pytest.param(
                {"sphere": 1.5},
                "+1.50 DS",
                does_not_raise(),
                None,
                id="Normal input sphere only",
            ),
            pytest.param(
                {"sphere": 1, "cyliner": -1, "axis": 190},
                None,
                pytest.raises(PrescriptionError),
                "Axis must be between 0 and 180 degrees",
                id="ERROR Axis range",
            ),
            pytest.param(
                {
                    "sphere": 1,
                    "cylinder": -1,
                    "axis": 90,
                    "add": {"add": -1.00},
                },
                None,
                pytest.raises(PrescriptionError),
                "Add must be a positive number",
                id="ERROR Add range",
            ),
            pytest.param(
                {
                    "sphere": 1,
                    "cylinder": -1,
                    "axis": 90,
                    "add": {"add": +1.00, "working_distance_cm": 601},
                },
                None,
                pytest.raises(PrescriptionError),
                "Working Distance (cm) must be greater than 0 cm and no greater than 600cm",
                id="ERROR Working distance range",
            ),
        ],
    )
    def test_initialising_object(
        self, test_input, expected, exception, exception_message
    ):
        """Test creating an object from the class."""
        with exception as excinfo:
            prescription = Prescription(**test_input)
            assert str(prescription) == expected
        if excinfo is not None:
            assert excinfo.value.message == exception_message

    @pytest.mark.parametrize(
        "test_prescription,test_input,expected,exception,exception_message",
        [
            pytest.param(
                Prescription(sphere=1, cylinder=-1, axis=90),
                None,
                Prescription(sphere=0, cylinder=+1, axis=180),
                does_not_raise(),
                None,
                id="Normal input",
            ),
            pytest.param(
                Prescription(sphere=1, cylinder=-1, axis=90),
                "n",
                Prescription(sphere=1, cylinder=-1, axis=90),
                does_not_raise(),
                None,
                id="n flag",
            ),
            pytest.param(
                Prescription(sphere=1, cylinder=-1, axis=90),
                "p",
                Prescription(sphere=0, cylinder=+1, axis=180),
                does_not_raise(),
                None,
                id="p flag",
            ),
            pytest.param(
                Prescription(sphere=1, cylinder=+0.75, axis=180),
                None,
                Prescription(sphere=+1.75, cylinder=-0.75, axis=90),
                does_not_raise(),
                None,
                id="positive cyl",
            ),
            pytest.param(
                Prescription(sphere=1, cylinder=+0.75, axis=180),
                "wrong flag",
                None,
                pytest.raises(PrescriptionError),
                "Method transpose() only accepts 'n' and 'p' as input flags",
                id="ERROR flag",
            ),
        ],
    )
    def test_transpose(
        self,
        test_prescription,
        test_input,
        expected,
        exception,
        exception_message,
    ):
        """Test transpose() method and flags."""
        with exception as excinfo:
            if test_input is None:
                test_prescription.transpose()
            else:
                test_prescription.transpose(test_input)
            assert test_prescription.sphere == expected.sphere
            assert test_prescription.cylinder == expected.cylinder
            assert test_prescription.axis == expected.axis
        if excinfo is not None:
            assert excinfo.value.message == exception_message

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            pytest.param(
                Prescription(sphere=2, cylinder=-4),
                0,
            ),
            pytest.param(
                Prescription(sphere=1, cylinder=-4),
                -1,
            ),
            pytest.param(
                Prescription(sphere=+5, cylinder=+10),
                10,
            ),
        ],
    )
    def test_mean_sphere(self, test_input, expected):
        """Test mean_sphere property."""
        assert test_input.mean_sphere == expected

    @pytest.mark.parametrize(
        "test_input,test_efficient,expected,exception,exception_message",
        [
            pytest.param(
                "+1.00/-1.00x90",
                None,
                Prescription(sphere=1, cylinder=-1, axis=90),
                does_not_raise(),
                None,
                id="Normal input",
            ),
            pytest.param(
                "+1.00/-1.00x90",
                False,
                Prescription(sphere=1, cylinder=-1, axis=90),
                does_not_raise(),
                None,
                id="Normal input",
            ),
            pytest.param(
                "pl/-1.00x90",
                False,
                Prescription(sphere=0, cylinder=-1, axis=90),
                does_not_raise(),
                None,
                id="Normal input",
            ),
            pytest.param(
                "plano/-1.00x90",
                False,
                Prescription(sphere=0, cylinder=-1, axis=90),
                does_not_raise(),
                None,
                id="Normal input",
            ),
        ],
    )
    def test_parse(
        self,
        test_input,
        test_efficient,
        expected,
        exception,
        exception_message,
    ):
        """Test transpose() method and flags."""
        with exception as excinfo:
            if test_efficient is None:
                rx = Prescription().parse(test_input)
            else:
                rx = Prescription().parse(test_input, efficient_parser=test_efficient)
            assert rx == expected
        if excinfo is not None:
            assert excinfo.value.message == exception_message
