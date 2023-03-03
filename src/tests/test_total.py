"""
Unit tests for the functions in the size prediction module
Author: Kenneth Schackart <schackartk1@gmail.com>
"""

import pytest

from t_junction_model import total


# -------------------------------------------------------------------------------------
def test_calc_nondim_total_volume() -> None:
    """Test calc_nondim_total_volume()"""

    height = 33 * 10**-6
    width = 100 * 10**-6
    inlet_width = 100 * 10**-6
    epsilon = 0.1 * width
    flow_cont = 3 * 10**-9
    flow_disp = 2 * flow_cont
    flow_gutter = 0.1 * flow_cont

    # Calculated manually
    exp_vol = 5.2997388

    calc_vol = total.calc_nondim_total_volume(
        height, width, inlet_width, epsilon, flow_cont, flow_disp, flow_gutter
    )

    assert calc_vol == pytest.approx(exp_vol)

    height = 0

    calc_vol = total.calc_nondim_total_volume(
        height, width, inlet_width, epsilon, flow_cont, flow_disp, flow_gutter
    )

    assert calc_vol is None


# -------------------------------------------------------------------------------------
def test_calc_total_volume() -> None:
    """Test calc_total_volume()"""

    height = 33 * 10**-6
    width = 100 * 10**-6
    inlet_width = 100 * 10**-6
    epsilon = 0.1 * width
    flow_cont = 3 * 10**-9
    flow_disp = 2 * flow_cont
    flow_gutter = 0.1 * flow_cont

    nondim_volume = total.calc_nondim_total_volume(
        height, width, inlet_width, epsilon, flow_cont, flow_disp, flow_gutter
    )

    assert nondim_volume is not None

    assert total.calc_total_volume(
        height, width, inlet_width, epsilon, flow_cont, flow_disp, flow_gutter
    ) == pytest.approx(nondim_volume * height * width**2)
