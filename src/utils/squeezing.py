"""
Purpose: Define functions used during the squeezing phase
Author:  Kenneth Schackart <schackartk1@gmail.com>
Date:    7 November 2022
"""

import math
from math import pi as PI

import pytest


# -------------------------------------------------------------------------------------
def calc_squeezing_volume(height: float, width: float, inlet_width: float,
                          epsilon: float, flow_cont: float, flow_disp: float,
                          flow_gutter: float) -> float:
    """
    Calculate the volume of the droplet due to squeezing phase

    Arguments:
    `height`: channel height
    `width`: channel width
    `inlet_width`: inlet channel width
    `epsilon`: corner roundness
    `flow_cont`: volumetric flow rate of continuous phase
    `flow_disp`: volumetric flow rate of dispersed phase
    `flow_gutter`: volumetric flow rate of gutter
    """

    alpha = calc_alpha(height, width, inlet_width, epsilon, flow_cont,
                       flow_gutter)

    squeezing_volume = alpha * height * (width**2) * (flow_disp / flow_cont)

    return squeezing_volume


# -------------------------------------------------------------------------------------
def calc_alpha(height: float, width: float, inlet_width: float, epsilon: float,
               flow_cont: float, flow_gutter: float) -> float:
    """
    Calculate the sequeezing coefficient, alpha

    Arguments:
    `height`: channel height
    `width`: channel width
    `inlet_width`: inlet channel width
    `epsilon`: corner roundness
    `flow_cont`: volumetric flow rate of continuous phase
    `flow_gutter`: volumetric flow rate of gutter
    """

    fill_radius = calc_fill_radius(width, inlet_width)
    pinch_radius = calc_pinch_radius(height, width, inlet_width, epsilon)

    const = (1 - (PI / 4))
    flow_ratio = 1 - (flow_gutter / flow_cont)
    geometries = ((pinch_radius / width)**2) - (
        (fill_radius / width)**2) + (PI / 4) * (height / width) * (
            (pinch_radius / width) - (fill_radius / width))

    alpha = const * geometries / flow_ratio

    return alpha


# -------------------------------------------------------------------------------------
def test_calc_alpha() -> None:
    """ Test calc_alpha() """


# -------------------------------------------------------------------------------------
def calc_fill_radius(width: float, inlet_width: float) -> float:
    """
    Calculate the fill radius, which is the greater of the two channel widths

    Arguments:
    `width`: channel width
    `inlet_width`: inlet channel width
    """

    return max([width, inlet_width])


# -------------------------------------------------------------------------------------
def test_calc_fill_radius() -> None:
    """ Test calc_fill_radius() """

    assert calc_fill_radius(3., 2.) == 3.
    assert calc_fill_radius(1.7, 2.1) == 2.1


# -------------------------------------------------------------------------------------
def calc_pinch_radius(height: float, width: float, inlet_width: float,
                      epsilon: float):
    """
    Calculate the pinching radius

    Arguments:
    `height`: channel height
    `width`: channel width
    `inlet_width`: inlet channel width
    `epsilon`: corner roundness
    """

    pinch_width = calc_pinch_width(height, width, epsilon)

    pinch_radius = width + inlet_width - pinch_width + math.sqrt(
        2 * (inlet_width - pinch_width) * (width - pinch_width))

    return pinch_radius


# -------------------------------------------------------------------------------------
def test_calc_pinch_radius() -> None:
    """ Test calc_pinch_radius() """

    height = 3.
    width = 7.
    inlet_width = 5.
    epsilon = 2.

    # Equation in paper
    expected_pinch_radius = width + inlet_width - (
        (height * width / (height + width)) - epsilon) + math.sqrt(
            2 * (inlet_width - ((height * width /
                                 (height + width)) - epsilon)) *
            (width - ((height * width / (height + width)) - epsilon)))

    assert calc_pinch_radius(height, width, inlet_width,
                             epsilon) == expected_pinch_radius


# -------------------------------------------------------------------------------------
def calc_pinch_width(height: float, width: float, epsilon: float) -> float:
    """
    Calculate "pinch width" the width of dispersed phase at punching if corner weren't
    rounded

    Arguments:
    `height`: channel height
    `width`: channel width
    `epsilon`: corner roundness
    """

    small_r_pinch = 0.5 * height * width / (height + width)
    pinch_width = 2 * small_r_pinch - epsilon

    return pinch_width


# -------------------------------------------------------------------------------------
def test_calc_pinch_width() -> None:
    """ Test calc_pinch_width() """

    height = 3.
    width = 7.
    epsilon = 2.

    expected_pinch_width = (height * width / (height + width)) - epsilon

    assert calc_pinch_width(height, width, epsilon) == expected_pinch_width
    assert calc_pinch_width(height, width, epsilon) == pytest.approx(0.1)
