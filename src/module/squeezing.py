"""
Squeezing
~~~
Define functions used during the squeezing phase
Author: Kenneth Schackart <schackartk1@gmail.com>
"""

import math
from math import pi as PI


# -------------------------------------------------------------------------------------
def calc_nondim_squeeze_volume(
    height: float,
    width: float,
    inlet_width: float,
    epsilon: float,
    flow_cont: float,
    flow_disp: float,
    flow_gutter: float,
) -> float:
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

    squeeze_volume = calc_squeezing_volume(
        height, width, inlet_width, epsilon, flow_cont, flow_disp, flow_gutter
    )

    nondim_volume = squeeze_volume / (height * (width**2))

    return nondim_volume


# -------------------------------------------------------------------------------------
def calc_squeezing_volume(
    height: float,
    width: float,
    inlet_width: float,
    epsilon: float,
    flow_cont: float,
    flow_disp: float,
    flow_gutter: float,
) -> float:
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

    alpha = _calc_alpha(height, width, inlet_width, epsilon, flow_cont, flow_gutter)

    squeezing_volume = alpha * height * (width**2) * (flow_disp / flow_cont)

    return squeezing_volume


# -------------------------------------------------------------------------------------
def _calc_alpha(
    height: float,
    width: float,
    inlet_width: float,
    epsilon: float,
    flow_cont: float,
    flow_gutter: float,
) -> float:
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

    fill_radius = _calc_fill_radius(width, inlet_width)
    pinch_radius = _calc_pinch_radius(height, width, inlet_width, epsilon)

    const = 1 - (PI / 4)
    flow_ratio = 1 - (flow_gutter / flow_cont)
    geometries = (
        ((pinch_radius / width) ** 2)
        - ((fill_radius / width) ** 2)
        + (PI / 4) * (height / width) * ((pinch_radius / width) - (fill_radius / width))
    )

    alpha = const * geometries / flow_ratio

    return alpha


# -------------------------------------------------------------------------------------
def _calc_fill_radius(width: float, inlet_width: float) -> float:
    """
    Calculate the fill radius, which is the greater of the two channel widths

    Arguments:
    `width`: channel width
    `inlet_width`: inlet channel width
    """

    return max([width, inlet_width])


# -------------------------------------------------------------------------------------
def _calc_pinch_radius(height: float, width: float, inlet_width: float, epsilon: float):
    """
    Calculate the pinching radius

    Arguments:
    `height`: channel height
    `width`: channel width
    `inlet_width`: inlet channel width
    `epsilon`: corner roundness
    """

    pinch_width = _calc_pinch_width(height, width, epsilon)

    pinch_radius = (
        width
        + inlet_width
        - pinch_width
        + math.sqrt(2 * (inlet_width - pinch_width) * (width - pinch_width))
    )

    return pinch_radius


# -------------------------------------------------------------------------------------
def _calc_pinch_width(height: float, width: float, epsilon: float) -> float:
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
def _calc_radius(
    height: float,
    width: float,
    inlet_widt: float,
    flow_cont: float,
    flow_gutter: float,
    time: float,
) -> float:
    """
    Calculate the radius (big R) as a function of time

    Arguements:
    `height`: channel height
    `width`: channel width
    `inlet_width`: inlet channel width
    `flow_cont`: volumetric flow rate of continuous phase
    `flow_gutter`: volumetric flow rate of gutter
    `time`: time since begin of squeezing phase
    """

    # Equation for R is a quadratic equation of the form
    # a*R^2 + b*R + c = 0

    r_fill = _calc_fill_radius(width, inlet_widt)

    # Assign coefficients of quadratic equation
    coeff_a = 1
    coeff_b = (PI * height) / 4
    coeff_c = -1 * (
        r_fill**2
        + (coeff_b * r_fill)
        + (
            time
            * (flow_cont / height)
            * (1 - (flow_gutter / flow_cont))
            / (1 - (PI / 4))
        )
    )

    radius = (1 / 2) * (
        (-1 * coeff_b) + math.sqrt((coeff_b**2) - 4 * coeff_a * coeff_c)
    )

    return radius


# -------------------------------------------------------------------------------------
def _calc_2r(
    height: float,
    width: float,
    inlet_width: float,
    epsilon: float,
    flow_cont: float,
    flow_gutter: float,
    time: float,
) -> float:
    """
    Calculate the 2r (minimal distance between interface and junction)
    as a function of time

    Arguements:
    `height`: channel height
    `width`: channel width
    `inlet_width`: inlet channel width
    `epsilon`: corner roundness
    `flow_cont`: volumetric flow rate of continuous phase
    `flow_gutter`: volumetric flow rate of gutter
    `time`: time since begin of squeezing phase
    """

    radius = _calc_radius(height, width, inlet_width, flow_cont, flow_gutter, time)

    two_r = (
        radius
        - math.sqrt((radius - width) ** 2 + (radius - inlet_width) ** 2)
        + epsilon
    )

    return two_r
