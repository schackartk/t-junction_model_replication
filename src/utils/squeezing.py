"""
Squeezing
~~~
Define functions used during the squeezing phase
Author: Kenneth Schackart <schackartk1@gmail.com>
"""

import math
from math import pi as PI

import pytest


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

    alpha = calc_alpha(height, width, inlet_width, epsilon, flow_cont, flow_gutter)

    squeezing_volume = alpha * height * (width**2) * (flow_disp / flow_cont)

    return squeezing_volume


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
def test_calc_nondim_squeeze_volume() -> None:
    """Test calc_nondim_squeeze_volume()"""

    height = 1.0
    width = 7.0
    inlet_width = 5.0
    epsilon = 0.1
    flow_cont = 6.0
    flow_gutter = 0.5
    flow_disp = 3.0

    alpha = calc_alpha(height, width, inlet_width, epsilon, flow_cont, flow_gutter)

    expected_nondim_vol = alpha * flow_disp / flow_cont

    assert calc_nondim_squeeze_volume(
        height, width, inlet_width, epsilon, flow_cont, flow_disp, flow_gutter
    ) == pytest.approx(expected_nondim_vol)


# -------------------------------------------------------------------------------------
def calc_alpha(
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

    fill_radius = calc_fill_radius(width, inlet_width)
    pinch_radius = calc_pinch_radius(height, width, inlet_width, epsilon)

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
def test_calc_alpha() -> None:
    """Test calc_alpha()"""

    height = 0.5
    width = 1.0
    inlet_width = 2 / 3
    epsilon = 0.0
    flow_cont = 1.0
    flow_gutter = 0.1

    assert calc_alpha(
        height, width, inlet_width, epsilon, flow_cont, flow_gutter
    ) == pytest.approx(0.808977)

    inlet_width = 2.0

    assert calc_alpha(
        height, width, inlet_width, epsilon, flow_cont, flow_gutter
    ) == pytest.approx(3.369487)


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
    """Test calc_fill_radius()"""

    assert calc_fill_radius(3.0, 2.0) == 3.0
    assert calc_fill_radius(1.7, 2.1) == 2.1


# -------------------------------------------------------------------------------------
def calc_pinch_radius(height: float, width: float, inlet_width: float, epsilon: float):
    """
    Calculate the pinching radius

    Arguments:
    `height`: channel height
    `width`: channel width
    `inlet_width`: inlet channel width
    `epsilon`: corner roundness
    """

    pinch_width = calc_pinch_width(height, width, epsilon)

    pinch_radius = (
        width
        + inlet_width
        - pinch_width
        + math.sqrt(2 * (inlet_width - pinch_width) * (width - pinch_width))
    )

    return pinch_radius


# -------------------------------------------------------------------------------------
def test_calc_pinch_radius() -> None:
    """Test calc_pinch_radius()"""

    height = 3.0
    width = 7.0
    inlet_width = 5.0
    epsilon = 2.0

    # Equation in paper
    expected_pinch_radius = (
        width
        + inlet_width
        - ((height * width / (height + width)) - epsilon)
        + math.sqrt(
            2
            * (inlet_width - ((height * width / (height + width)) - epsilon))
            * (width - ((height * width / (height + width)) - epsilon))
        )
    )

    assert (
        calc_pinch_radius(height, width, inlet_width, epsilon) == expected_pinch_radius
    )


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
    """Test calc_pinch_width()"""

    height = 3.0
    width = 7.0
    epsilon = 2.0

    expected_pinch_width = (height * width / (height + width)) - epsilon

    assert calc_pinch_width(height, width, epsilon) == expected_pinch_width
    assert calc_pinch_width(height, width, epsilon) == pytest.approx(0.1)


# -------------------------------------------------------------------------------------
def calc_radius(
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

    r_fill = calc_fill_radius(width, inlet_widt)

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
def test_calc_radius() -> None:
    """Test calc_radius()"""

    height = 33 * 10**-6
    width = 100 * 10**-6
    inlet_width = width
    continuous_flow = 3 * 10**-9
    gutter_flow = 0.1 * continuous_flow

    fill_radius = calc_fill_radius(width, inlet_width)

    assert (
        calc_radius(height, width, inlet_width, continuous_flow, gutter_flow, 0)
        == fill_radius
    )

    assert (
        calc_radius(height, width, inlet_width, continuous_flow, gutter_flow, 0.01)
        > fill_radius
    )

    assert calc_radius(
        height, width, inlet_width, continuous_flow, gutter_flow, 0.05
    ) == pytest.approx(0.004354597078)


# -------------------------------------------------------------------------------------
def calc_2r(
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

    radius = calc_radius(height, width, inlet_width, flow_cont, flow_gutter, time)

    two_r = (
        radius
        - math.sqrt((radius - width) ** 2 + (radius - inlet_width) ** 2)
        + epsilon
    )

    return two_r


# -------------------------------------------------------------------------------------
def test_calc_2r() -> None:
    """Test calc_2r()"""

    height = 33 * 10**-6
    width = 100 * 10**-6
    inlet_width = width
    continuous_flow = 3 * 10**-9
    gutter_flow = 0.1 * continuous_flow
    epsilon = 0.1 * width

    fill_radius = calc_fill_radius(width, inlet_width)

    assert calc_2r(
        height, width, inlet_width, epsilon, continuous_flow, gutter_flow, 0
    ) == pytest.approx(fill_radius + epsilon)

    assert (
        calc_2r(
            height, width, inlet_width, epsilon, continuous_flow, gutter_flow, 0.0001
        )
        < fill_radius + epsilon
    )

    assert calc_2r(
        height, width, inlet_width, epsilon, continuous_flow, gutter_flow, 0.00001
    ) == pytest.approx(0.0001034660)
