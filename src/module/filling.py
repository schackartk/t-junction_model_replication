"""
Filling
~~~
Define functions used during the filling phase
Author: Kenneth Schackart <schackartk1@gmail.com>
"""

import math
from math import pi as PI
from typing import Optional


# -------------------------------------------------------------------------------------
def _calc_gross_volume(height: float, area: float) -> float:
    """
    Calculate the gross volume of the droplet (before subtracting gutters)

    Arguments:
    `height`: channel height
    `area`: droplet area
    """

    return height * area


# -------------------------------------------------------------------------------------
def _calc_gutter_area(height: float) -> float:
    """
    Calculate the cross-sectional area of a gutter

    Arguments:
    `height`: Channel height
    """

    corner_area = (height / 2) ** 2
    droplet_area = 0.25 * PI * (height / 2) ** 2
    gutter_area = corner_area - droplet_area

    return gutter_area


# -------------------------------------------------------------------------------------
def _calc_gutter_volume(height: float, gutter_length: float) -> float:
    """
    Calculate the volume of an individual gutter

    Arguments:
    `gutter_area`: cross sectional area of gutter
    `gutter_length`: length of gutter (droplet perimeter)
    """

    gutter_area = _calc_gutter_area(height)

    return gutter_area * gutter_length


# -------------------------------------------------------------------------------------
def _calc_circle_fraction_area(radius: float, portion: float) -> float:
    """
    Calculate a fraction of the area of a circle

    Arguments:
    `diameter`: circle radius
    `portion`: Portion of circle area as decimal
    """

    return portion * PI * radius**2


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
        area = _calc_circle_fraction_area(width, 0.25) + _calc_circle_fraction_area(
            width / 2, 0.5
        )

        # Gutter length
        quarter_circle_length = 0.25 * PI * 2 * width
        half_circle_length = 0.5 * PI * width
        gutter_length = quarter_circle_length + half_circle_length

        fill_volume = _calc_gross_volume(height, area) - 2 * _calc_gutter_volume(
            height, gutter_length
        )

    else:
        # Mid-plane area and volume
        right_triangle_area = (
            0.5
            * (inlet_width - width)
            * (inlet_width**2 - (inlet_width - width) ** 2) ** 0.5
        )
        sector_area = (
            (inlet_width**2) * 0.5 * math.asin((inlet_width - width) / inlet_width)
        )

        area_in_inlet = right_triangle_area + sector_area
        quarter_circle_in_channel = (
            _calc_circle_fraction_area(inlet_width, 0.25) - area_in_inlet
        )
        area = _calc_circle_fraction_area(width / 2, 0.5) + quarter_circle_in_channel

        # Gutter length and volume
        half_circle_length = 0.5 * PI * width
        arc_length = inlet_width * ((PI / 2) - math.asin(1 - (width / inlet_width)))
        gutter_length = half_circle_length + arc_length

        fill_volume = _calc_gross_volume(height, area) - 2 * _calc_gutter_volume(
            height, gutter_length
        )

    return fill_volume


# -------------------------------------------------------------------------------------
def calc_incorrect_fill_volume(
    height: float, width: float, inlet_width: float
) -> float:
    """
    Calculate the filling volume using modified (incorrect) equation to reproduce
    figure 2a exactly.

    Arguments:
    `height`: channel height
    `width`: channel width
    `inlet_width`: inlet channel width
    """

    if inlet_width <= width:
        # No mistake in equation, use correct version
        fill_volume = calc_fill_volume(height, width, inlet_width)

    else:
        # First and second terms are correct
        # pylint: disable=R0801
        first_term = (
            (PI / 4) - 0.5 * math.asin(1 - (width / inlet_width))
        ) * (  # pylint: disable=duplicate-code
            inlet_width / width
        ) ** 2

        second_term = (-0.5) * ((inlet_width / width) - 1) * (
            2 * (inlet_width / width) - 1
        ) ** 0.5 + (PI / 8)

        # Third term is missing parentheses
        third_term = (
            (-0.5)
            * (1 - (PI / 4))
            * (
                (PI / 2)
                - math.asin(1 - (width / inlet_width)) * (inlet_width / width)
                + (PI / 2)
            )
            * (height / width)
        )

        nondim_fill_volume = first_term + second_term + third_term
        fill_volume = nondim_fill_volume * (height * width**2)

    return fill_volume


# -------------------------------------------------------------------------------------
def calc_nondim_fill_volume(
    height: float, width: float, inlet_width: float
) -> Optional[float]:
    """
    Calculate the non-dimensionalized fill volume

    Arguments:
    `height`: channel height
    `width`: channel width
    `inlet_width`: inlet channel width
    """

    if 0 in [height, width, inlet_width]:
        return None

    fill_volume = calc_fill_volume(height, width, inlet_width)

    non_dim_volume = fill_volume / (height * width**2)

    return non_dim_volume


# -------------------------------------------------------------------------------------
def calc_incorrect_nondim_fill_volume(
    height: float, width: float, inlet_width: float
) -> Optional[float]:
    """
    Calculate the non-dimensionalized fill volume using the incorrect equation
    in order to reproduce figure 2a exactly

    Arguments:
    `height`: channel height
    `width`: channel width
    `inlet_width`: inlet channel width
    """

    if 0 in [height, width, inlet_width]:
        return None

    fill_volume = calc_incorrect_fill_volume(height, width, inlet_width)

    non_dim_volume = fill_volume / (height * width**2)

    return non_dim_volume
