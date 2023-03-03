"""
T-junction droplet/bubble size prediction
~~~
This module contains the functions for predicting the total
volume of droplets/bubbles produced in a microfluidic T-junction.

Author: Kenneth Schackart <schackartk1@gmail.com>
"""

from typing import Optional

from t_junction_model import filling
from t_junction_model import squeezing


# -------------------------------------------------------------------------------------
def calc_nondim_total_volume(
    height: float,
    width: float,
    inlet_width: float,
    epsilon: float,
    flow_cont: float,
    flow_disp: float,
    flow_gutter: float,
) -> Optional[float]:
    """
    Calculate the non-dimensionalized total volume of droplet/bubble

    Arguments:
    `height`: channel height
    `width`: channel width
    `inlet_width`: inlet channel width
    `epsilon`: corner roundness
    `flow_cont`: volumetric flow rate of continuous phase
    `flow_disp`: volumetric flow rate of dispersed phase
    `flow_gutter`: volumetric flow rate of gutter
    """

    nondim_fill_volume = filling.calc_nondim_fill_volume(height, width, inlet_width)
    nondim_squeeze_volume = squeezing.calc_nondim_squeeze_volume(
        height, width, inlet_width, epsilon, flow_cont, flow_disp, flow_gutter
    )

    if nondim_fill_volume is None or nondim_squeeze_volume is None:
        return None

    return nondim_fill_volume + nondim_squeeze_volume


# -------------------------------------------------------------------------------------
def calc_total_volume(
    height: float,
    width: float,
    inlet_width: float,
    epsilon: float,
    flow_cont: float,
    flow_disp: float,
    flow_gutter: float,
) -> float:
    """
    Calculate the total volume of droplet/bubble

    Arguments:
    `height`: channel height
    `width`: channel width
    `inlet_width`: inlet channel width
    `epsilon`: corner roundness
    `flow_cont`: volumetric flow rate of continuous phase
    `flow_disp`: volumetric flow rate of dispersed phase
    `flow_gutter`: volumetric flow rate of gutter
    """

    fill_volume = filling.calc_fill_volume(height, width, inlet_width)
    squeeze_volume = squeezing.calc_squeezing_volume(
        height, width, inlet_width, epsilon, flow_cont, flow_disp, flow_gutter
    )

    return fill_volume + squeeze_volume
