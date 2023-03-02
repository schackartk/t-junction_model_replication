"""
Unit tests for the functions in the squeezing module
Author: Kenneth Schackart <schackartk1@gmail.com>
"""

import math
import pytest

from module import squeezing

# pylint: disable=protected-access


# -------------------------------------------------------------------------------------
def test_calc_alpha() -> None:
    """Test _calc_alpha()"""

    height = 0.5
    width = 1.0
    inlet_width = 2 / 3
    epsilon = 0.0
    flow_cont = 1.0
    flow_gutter = 0.1

    assert squeezing._calc_alpha(
        height, width, inlet_width, epsilon, flow_cont, flow_gutter
    ) == pytest.approx(0.808977)

    inlet_width = 2.0

    assert squeezing._calc_alpha(
        height, width, inlet_width, epsilon, flow_cont, flow_gutter
    ) == pytest.approx(3.369487)


# -------------------------------------------------------------------------------------
def test_calc_fill_radius() -> None:
    """Test _calc_fill_radius()"""

    assert squeezing._calc_fill_radius(3.0, 2.0) == 3.0
    assert squeezing._calc_fill_radius(1.7, 2.1) == 2.1


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

    alpha = squeezing._calc_alpha(
        height, width, inlet_width, epsilon, flow_cont, flow_gutter
    )

    expected_nondim_vol = alpha * flow_disp / flow_cont

    assert squeezing.calc_nondim_squeeze_volume(
        height, width, inlet_width, epsilon, flow_cont, flow_disp, flow_gutter
    ) == pytest.approx(expected_nondim_vol)


# -------------------------------------------------------------------------------------
def test_calc_pinch_radius() -> None:
    """Test _calc_pinch_radius()"""

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
        squeezing._calc_pinch_radius(height, width, inlet_width, epsilon)
        == expected_pinch_radius
    )


# -------------------------------------------------------------------------------------
def test_calc_pinch_width() -> None:
    """Test _calc_pinch_width()"""

    height = 3.0
    width = 7.0
    epsilon = 2.0

    expected_pinch_width = (height * width / (height + width)) - epsilon

    assert squeezing._calc_pinch_width(height, width, epsilon) == expected_pinch_width
    assert squeezing._calc_pinch_width(height, width, epsilon) == pytest.approx(0.1)


# -------------------------------------------------------------------------------------
def test_calc_radius() -> None:
    """Test _calc_radius()"""

    height = 33 * 10**-6
    width = 100 * 10**-6
    inlet_width = width
    continuous_flow = 3 * 10**-9
    gutter_flow = 0.1 * continuous_flow

    fill_radius = squeezing._calc_fill_radius(width, inlet_width)

    assert (
        squeezing._calc_radius(
            height, width, inlet_width, continuous_flow, gutter_flow, 0
        )
        == fill_radius
    )

    assert (
        squeezing._calc_radius(
            height, width, inlet_width, continuous_flow, gutter_flow, 0.01
        )
        > fill_radius
    )

    assert squeezing._calc_radius(
        height, width, inlet_width, continuous_flow, gutter_flow, 0.05
    ) == pytest.approx(0.004354597078)


# -------------------------------------------------------------------------------------
def test_calc_2r() -> None:
    """Test _calc_2r()"""

    height = 33 * 10**-6
    width = 100 * 10**-6
    inlet_width = width
    continuous_flow = 3 * 10**-9
    gutter_flow = 0.1 * continuous_flow
    epsilon = 0.1 * width

    fill_radius = squeezing._calc_fill_radius(width, inlet_width)

    assert squeezing._calc_2r(
        height, width, inlet_width, epsilon, continuous_flow, gutter_flow, 0
    ) == pytest.approx(fill_radius + epsilon)

    assert (
        squeezing._calc_2r(
            height, width, inlet_width, epsilon, continuous_flow, gutter_flow, 0.0001
        )
        < fill_radius + epsilon
    )

    assert squeezing._calc_2r(
        height, width, inlet_width, epsilon, continuous_flow, gutter_flow, 0.00001
    ) == pytest.approx(0.0001034660)
