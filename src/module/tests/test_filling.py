"""
Unit tests for the functions in the filling module
Author: Kenneth Schackart <schackartk1@gmail.com>
"""

import math
from math import pi as PI

import pytest

from module import filling

# pylint: disable=protected-access


# -------------------------------------------------------------------------------------
def test_calc_gross_volume() -> None:
    """Test _calc_gross_volume()"""

    assert filling._calc_gross_volume(3.0, 7.0) == pytest.approx(21.0)
    assert filling._calc_gross_volume(4.0, 5.0) == pytest.approx(20.0)


# -------------------------------------------------------------------------------------
def test_calc_gutter_area() -> None:
    """Test _calc_gutter_area()"""

    assert filling._calc_gutter_area(1) == pytest.approx(0.25 * (1 - PI / 4))
    assert filling._calc_gutter_area(2) == pytest.approx(1 - PI / 4)


# -------------------------------------------------------------------------------------
def test_calc_gutter_volume() -> None:
    """Test _calc_gutter_volume()"""

    assert filling._calc_gutter_volume(1, 4) == pytest.approx(1 - PI / 4)
    assert filling._calc_gutter_volume(2, 8) == pytest.approx(8 - 2 * PI)


# -------------------------------------------------------------------------------------
def test_calc_circle_fraction_area() -> None:
    """Test _calc_circle_fraction_area()"""

    radius = 2

    portion = 0.5
    exp = 6.283185
    assert filling._calc_circle_fraction_area(radius, portion) == pytest.approx(exp)

    portion = 0.25
    exp = 3.14159
    assert filling._calc_circle_fraction_area(radius, portion) == pytest.approx(exp)


# -------------------------------------------------------------------------------------
def test_calc_fill_volume() -> None:
    """Test calc_fill_volume"""

    height = 2.0
    width = 3.0
    inlet_width = 1.0

    # Check output using simplified formula, given in paper
    exp_out = (((3 * PI) / 8) - (PI / 2) * (1 - (PI / 4)) * (height / width)) * (
        height * width**2
    )
    actual_out = filling.calc_fill_volume(height, width, inlet_width)

    assert actual_out == pytest.approx(exp_out)

    # Check output using simplified formula, given in paper
    height = 2.0
    width = 3.0
    inlet_width = 4.0

    first_term = ((PI / 4) - 0.5 * math.asin(1 - (width / inlet_width))) * (
        inlet_width / width
    ) ** 2

    second_term = (-0.5) * ((inlet_width / width) - 1) * (
        2 * (inlet_width / width) - 1
    ) ** 0.5 + (PI / 8)

    third_term = (
        (-0.5)
        * (1 - (PI / 4))
        * (
            ((PI / 2) - math.asin(1 - (width / inlet_width))) * (inlet_width / width)
            + (PI / 2)
        )
        * (height / width)
    )

    sum_of_terms = first_term + second_term + third_term

    exp_out = sum_of_terms * (height * width**2)

    actual_out = filling.calc_fill_volume(height, width, inlet_width)

    assert actual_out == pytest.approx(exp_out)


# -------------------------------------------------------------------------------------
def test_calc_incorrect_fill_volume() -> None:
    """Test calc_incorrect_fill_volume()"""

    height = 10.0
    width = 20.0

    # Functions are same if inlet_width <= width
    assert filling.calc_fill_volume(
        height, width, width - 2.0
    ) == filling.calc_incorrect_fill_volume(height, width, width - 2.0)
    assert filling.calc_fill_volume(
        height, width, width
    ) == filling.calc_incorrect_fill_volume(height, width, width)

    # Functions are different if inlet_width > width
    assert filling.calc_fill_volume(
        height, width, width * 2.0
    ) != filling.calc_incorrect_fill_volume(height, width, width * 2.0)

    # Incorrect function gives volume greater than should to be
    assert filling.calc_fill_volume(
        height, width, width * 2.0
    ) < filling.calc_incorrect_fill_volume(height, width, width * 2.0)


# -------------------------------------------------------------------------------------
def test_calc_nondim_fill_volume() -> None:
    """Test calc_nondim_fill_volume()"""

    height = 2.0
    width = 3.0
    inlet_width = 1.0

    # Check output using simplified formula, given in paper
    exp_out = ((3 * PI) / 8) - (PI / 2) * (1 - (PI / 4)) * (height / width)
    actual_out = filling.calc_nondim_fill_volume(height, width, inlet_width)

    assert actual_out == pytest.approx(exp_out)

    # Check output using simplified formula, given in paper
    height = 2.0
    width = 3.0
    inlet_width = 4.0

    first_term = ((PI / 4) - 0.5 * math.asin(1 - (width / inlet_width))) * (
        inlet_width / width
    ) ** 2

    second_term = (-0.5) * ((inlet_width / width) - 1) * (
        2 * (inlet_width / width) - 1
    ) ** 0.5 + (PI / 8)

    third_term = (
        (-0.5)
        * (1 - (PI / 4))
        * (
            ((PI / 2) - math.asin(1 - (width / inlet_width))) * (inlet_width / width)
            + (PI / 2)
        )
        * (height / width)
    )

    exp_out = first_term + second_term + third_term

    actual_out = filling.calc_nondim_fill_volume(height, width, inlet_width)

    assert actual_out == pytest.approx(exp_out)

    # returns None if any arguments are zero
    assert filling.calc_nondim_fill_volume(0.0, 1.0, 1.0) is None
    assert filling.calc_nondim_fill_volume(1.0, 0.0, 1.0) is None
    assert filling.calc_nondim_fill_volume(1.0, 1.0, 0.0) is None


# -------------------------------------------------------------------------------------
def test_calc_incorrect_nondim_fill_volume() -> None:
    """Test calc_incorrect_nondim_fill_volume()"""

    height = 10.0
    width = 20.0

    # returns None if any arguments are zero
    assert filling.calc_incorrect_nondim_fill_volume(0.0, 1.0, 1.0) is None
    assert filling.calc_incorrect_nondim_fill_volume(1.0, 0.0, 1.0) is None
    assert filling.calc_incorrect_nondim_fill_volume(1.0, 1.0, 0.0) is None

    # Functions are same if inlet_width <= width
    assert filling.calc_nondim_fill_volume(
        height, width, width - 2.0
    ) == filling.calc_incorrect_nondim_fill_volume(height, width, width - 2.0)
    assert filling.calc_nondim_fill_volume(
        height, width, width
    ) == filling.calc_incorrect_nondim_fill_volume(height, width, width)

    # Functions are different if inlet_width > width
    assert filling.calc_nondim_fill_volume(
        height, width, width * 2.0
    ) != filling.calc_incorrect_nondim_fill_volume(height, width, width * 2.0)

    # Incorrect function gives volume greater than should to be
    correct = filling.calc_nondim_fill_volume(height, width, width * 2.0)
    incorrect = filling.calc_incorrect_nondim_fill_volume(height, width, width * 2.0)
    assert correct is not None and incorrect is not None  # Must check before using "<"
    assert correct < incorrect
