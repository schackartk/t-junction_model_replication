"""
Purpose: Define functions used during the filling phase
Author:  Kenneth Schackart <schackartk1@gmail.com>
Date:    7 November 2022
"""

import math
from math import pi as PI

import pytest


# -------------------------------------------------------------------------------------
def calc_gross_volume(height: float, area: float) -> float:
    """
    Calculate the gross volume of the droplet (before subtracting gutters)

    Arguments:
    `height`: channel height
    `area`: droplet area
    """

    return height * area


# -------------------------------------------------------------------------------------
def test_calc_gross_volume() -> None:
    """ Test calc_gross_volume() """

    assert calc_gross_volume(3., 7.) == pytest.approx(21.)
    assert calc_gross_volume(4., 5.) == pytest.approx(20.)


# -------------------------------------------------------------------------------------
def calc_gutter_area(height: float) -> float:
    """
    Calculate the cross-sectional area of a gutter

    Arguments:
    `height`: Channel height
    """

    corner_area = (height / 2)**2
    droplet_area = 0.25 * PI * (height / 2)**2
    gutter_area = corner_area - droplet_area

    return gutter_area


# -------------------------------------------------------------------------------------
def test_calc_gutter_area() -> None:
    """ Test calc_gutter_area() """

    assert calc_gutter_area(1) == pytest.approx(0.25 * (1 - PI / 4))
    assert calc_gutter_area(2) == pytest.approx(1 - PI / 4)


# -------------------------------------------------------------------------------------
def calc_gutter_volume(height: float, gutter_length: float) -> float:
    """
    Calculate the volume of an individual gutter

    Arguments:
    `gutter_area`: cross sectional area of gutter
    `gutter_length`: length of gutter (droplet perimeter)
    """

    gutter_area = calc_gutter_area(height)

    return gutter_area * gutter_length


# -------------------------------------------------------------------------------------
def test_calc_gutter_volume() -> None:
    """ Test calc_gutter_volume() """

    assert calc_gutter_volume(1, 4) == pytest.approx(1 - PI / 4)
    assert calc_gutter_volume(2, 8) == pytest.approx(8 - 2 * PI)


# -------------------------------------------------------------------------------------
def calc_circle_fraction_area(radius: float, portion: float) -> float:
    """
    Calculate a fraction of the area of a circle

    Arguments:
    `diameter`: circle radius
    `portion`: Portion of circle area as decimal
    """

    return portion * PI * radius**2


# -------------------------------------------------------------------------------------
def test_calc_circle_fraction_area() -> None:
    """ Test calc_circle_fraction_area() """

    radius = 2

    portion = 0.5
    exp = 6.283185
    assert calc_circle_fraction_area(radius, portion) == pytest.approx(exp)

    portion = 0.25
    exp = 3.14159
    assert calc_circle_fraction_area(radius, portion) == pytest.approx(exp)


# -------------------------------------------------------------------------------------
def calc_fill_volume(height: float, width: float, inlet_width: float) -> float:
    """
    Calculate the filling volume

    Arguments:
    `height`: channel height
    `width`: channel width
    `inlet_width`: inlet channel width
    """

    if inlet_width <= width:
        # Mid-plane area
        area = calc_circle_fraction_area(
            width, 0.25) + calc_circle_fraction_area(width / 2, 0.5)

        # Gutter length
        quarter_circle_length = 0.25 * PI * 2 * width
        half_circle_length = 0.5 * PI * width
        gutter_length = quarter_circle_length + half_circle_length

        fill_volume = calc_gross_volume(
            height, area) - 2 * calc_gutter_volume(height, gutter_length)

    else:
        # Mid-plane area and volume
        right_triangle_area = 0.5 * (inlet_width -
                                     width) * (inlet_width**2 -
                                               (inlet_width - width)**2)**0.5
        sector_area = (inlet_width**2) * 0.5 * math.asin(
            (inlet_width - width) / inlet_width)

        area_in_inlet = right_triangle_area + sector_area
        quarter_circle_in_channel = calc_circle_fraction_area(
            inlet_width, 0.25) - area_in_inlet
        area = calc_circle_fraction_area(width / 2,
                                         0.5) + quarter_circle_in_channel

        # Gutter length and volume
        half_circle_length = 0.5 * PI * width
        arc_length = inlet_width * (
            (PI / 2) - math.asin(1 - (width / inlet_width)))
        gutter_length = half_circle_length + arc_length

        fill_volume = calc_gross_volume(
            height, area) - 2 * calc_gutter_volume(height, gutter_length)

    return fill_volume


# -------------------------------------------------------------------------------------
def test_calc_fill_volume() -> None:
    """ Test calc_fill_volume """

    height = 2.
    width = 3.
    inlet_width = 1.

    # Check output using simplified formula, given in paper
    exp_out = (((3 * PI) / 8) - (PI / 2) * (1 - (PI / 4)) *
               (height / width)) * (height * width**2)
    actual_out = calc_fill_volume(height, width, inlet_width)

    assert actual_out == pytest.approx(exp_out)

    # Check output using simplified formula, given in paper
    height = 2.
    width = 3.
    inlet_width = 4.

    first_term = ((PI / 4) - 0.5 * math.asin(1 - (width / inlet_width))) * (
        inlet_width / width)**2

    second_term = (-0.5) * (
        (inlet_width / width) - 1) * (2 *
                                      (inlet_width / width) - 1)**0.5 + (PI /
                                                                         8)

    third_term = (-0.5) * (1 - (PI / 4)) * (
        ((PI / 2) - math.asin(1 - (width / inlet_width))) *
        (inlet_width / width) + (PI / 2)) * (height / width)

    sum_of_terms = first_term + second_term + third_term

    exp_out = sum_of_terms * (height * width**2)

    actual_out = calc_fill_volume(height, width, inlet_width)

    assert actual_out == pytest.approx(exp_out)


# -------------------------------------------------------------------------------------
def calc_nondim_fill_volume(height: float, width: float,
                            inlet_width: float) -> float:
    """
    Calculate the non-dimensionalized fill volume

    Arguments:
    `height`: channel height
    `width`: channel width
    `inlet_width`: inlet channel width
    """

    fill_volume = calc_fill_volume(height, width, inlet_width)

    non_dim_volume = fill_volume / (height * width**2)

    return non_dim_volume


# -------------------------------------------------------------------------------------
def test_calc_nondim_fill_volume() -> None:
    """ Test calc_nondim_fill_volume() """

    height = 2.
    width = 3.
    inlet_width = 1.

    # Check output using simplified formula, given in paper
    exp_out = (((3 * PI) / 8) - (PI / 2) * (1 - (PI / 4)) * (height / width))
    actual_out = calc_nondim_fill_volume(height, width, inlet_width)

    assert actual_out == pytest.approx(exp_out)

    # Check output using simplified formula, given in paper
    height = 2.
    width = 3.
    inlet_width = 4.

    first_term = ((PI / 4) - 0.5 * math.asin(1 - (width / inlet_width))) * (
        inlet_width / width)**2

    second_term = (-0.5) * (
        (inlet_width / width) - 1) * (2 *
                                      (inlet_width / width) - 1)**0.5 + (PI /
                                                                         8)

    third_term = (-0.5) * (1 - (PI / 4)) * (
        ((PI / 2) - math.asin(1 - (width / inlet_width))) *
        (inlet_width / width) + (PI / 2)) * (height / width)

    exp_out = first_term + second_term + third_term

    actual_out = calc_nondim_fill_volume(height, width, inlet_width)

    assert actual_out == pytest.approx(exp_out)
