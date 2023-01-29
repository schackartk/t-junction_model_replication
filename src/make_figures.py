#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2023-01-29
Purpose: Generate figures from paper
"""

import argparse
import itertools
import os
from typing import NamedTuple

import pandas as pd
import plotnine as p9

from utils.filling import calc_nondim_fill_volume
from utils.formatter_class import CustomHelpFormatter
from utils.squeezing import calc_alpha, calc_nondim_squeeze_volume, calc_2r


class Args(NamedTuple):
    """Command-line arguments"""

    out_dir: str


# -------------------------------------------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Generate figures from paper", formatter_class=CustomHelpFormatter
    )

    parser.add_argument(
        "-o",
        "--out-dir",
        help="Output directory",
        metavar="DIR",
        type=str,
        default="figures/",
    )

    args = parser.parse_args()

    return Args(args.out_dir)


# -------------------------------------------------------------------------------------
def make_fig_2a(color_mapping: dict[str, str]) -> p9.ggplot:
    """
    Generate figure 2a: nondimensionalized volume during the filling phase
    plotted against channel height/width for 5 inlet width/width ratios

    Arguments:
    `color_mapping`: Dictionary mappying hex colors to width ratios
    """

    widths = [1.0]
    heights = map(lambda x: float(x / 1000), range(0, 501))
    inlet_widths = [1, 4 / 3, 2, 3]

    width_col = []
    height_col = []
    inlet_width_col = []
    for width, height, inlet_width in itertools.product(widths, heights, inlet_widths):
        width_col.append(width)
        height_col.append(height)
        inlet_width_col.append(inlet_width)

    filling_df = pd.DataFrame()
    filling_df["width"] = width_col
    filling_df["height"] = height_col
    filling_df["inlet_width"] = inlet_width_col

    filling_df["height_over_width"] = filling_df["height"] / filling_df["width"]
    filling_df["width_ratio"] = round(
        filling_df["inlet_width"] / filling_df["width"], 2
    )
    filling_df["width_ratio"] = filling_df["width_ratio"].astype(str)

    filling_df["nondim_vol"] = filling_df.apply(
        lambda row: calc_nondim_fill_volume(row.height, row.width, row.inlet_width),
        axis=1,
    )

    plot = (
        p9.ggplot(
            filling_df, p9.aes("height_over_width", "nondim_vol", color="width_ratio")
        )
        + p9.geom_line()
        + p9.scale_color_manual(color_mapping)
        + p9.scale_y_continuous(
            breaks=[tick / 10 for tick in list(range(0, 22, 2))], limits=[0, 2]
        )
        + p9.theme_light()
        + p9.labs(x="h/w", y="Dimensionless fill volume", color="w_in / w")
    )

    return plot


# -------------------------------------------------------------------------------------
def make_fig_2b(color_mapping: dict[str, str]) -> p9.ggplot:
    """
    Generate figure 2b: squeezing coefficient alpha
    plotted against channel height/width for 5 inlet width/width ratios

    Arguments:
    `color_mapping`: Dictionary mappying hex colors to width ratios
    """

    widths = [1.0]
    flow_ratio = 0.1
    epsilon = 0.0
    heights = map(lambda x: float(x / 100), range(0, 51))
    inlet_widths = [1 / 3, 2 / 3, 1, 4 / 3, 2, 3]

    width_col = []
    height_col = []
    inlet_width_col = []
    for width, height, inlet_width in itertools.product(widths, heights, inlet_widths):
        width_col.append(width)
        height_col.append(height)
        inlet_width_col.append(inlet_width)

    alpha_df = pd.DataFrame()
    alpha_df["width"] = width_col
    alpha_df["height"] = height_col
    alpha_df["inlet_width"] = inlet_width_col
    alpha_df["epsilon"] = epsilon
    alpha_df["flow_cont"] = 1.0
    alpha_df["flow_gutter"] = alpha_df["flow_cont"] * flow_ratio

    alpha_df["height_over_width"] = alpha_df["height"] / alpha_df["width"]
    alpha_df["width_ratio"] = round(alpha_df["inlet_width"] / alpha_df["width"], 2)
    alpha_df["width_ratio"] = alpha_df["width_ratio"].astype(str)

    alpha_df["alpha"] = alpha_df.apply(
        lambda row: calc_alpha(
            row.height,
            row.width,
            row.inlet_width,
            row.epsilon,
            row.flow_cont,
            row.flow_gutter,
        ),
        axis=1,
    )

    plot = (
        p9.ggplot(alpha_df, p9.aes("height_over_width", "alpha", color="width_ratio"))
        + p9.geom_line()
        + p9.scale_y_continuous(breaks=list(range(0, 9, 1)), limits=[0, 8])
        + p9.scale_color_manual(color_mapping)
        + p9.theme_light()
        + p9.labs(x="h/w", y="Squeezing coefficient", color="w_in / w")
    )

    return plot


# -------------------------------------------------------------------------------------
def make_fig_3(color_mapping: dict[str, str]) -> p9.ggplot:
    """
    Generate figure 3: dimensionless volume of bubbles and droplets
    against flow rate ratio for 5 width ratios

    Arguments:
    `color_mapping`: Dictionary mappying hex colors to width ratios
    """

    continuous_flow = 1.0
    gutter_flow = continuous_flow * 0.1
    width = 1.0
    inlet_widths = [1 / 3, 2 / 3, 1, 4 / 3, 3]
    dispersed_flows = list(map(lambda x: float(x / 10), range(0, 101)))

    # h/w is assigned based on width ratio
    height_dictionary = {
        "0.33": 1 / 3,
        "0.67": 0.11,
        "1.0": 1 / 3,
        "1.33": 0.17,
        "3.0": 1 / 3,
    }

    inlet_width_col = []
    dispersed_flow_col = []
    for inlet_width, dispersed_flow in itertools.product(inlet_widths, dispersed_flows):
        inlet_width_col.append(inlet_width)
        dispersed_flow_col.append(dispersed_flow)

    # Parameters for bubbles
    vol_df = pd.DataFrame()
    vol_df["inlet_width"] = inlet_width_col
    vol_df["dispersed_flow"] = dispersed_flow_col
    vol_df["width"] = width
    vol_df["continuous_flow"] = continuous_flow
    vol_df["gutter_flow"] = gutter_flow
    vol_df["type"] = "bubbles"

    vol_df["epsilon"] = 0.1 * vol_df["width"]
    vol_df["flow_ratio"] = vol_df["dispersed_flow"] / vol_df["continuous_flow"]
    vol_df["width_ratio"] = round(vol_df["inlet_width"] / vol_df["width"], 2)
    vol_df["width_ratio"] = vol_df["width_ratio"].astype(str)
    vol_df["height"] = vol_df.apply(
        lambda row: height_dictionary.get(row.width_ratio), axis=1
    )

    # Parameters for droplets
    liq_liq_df = pd.DataFrame()
    liq_liq_df["dispersed_flow"] = dispersed_flows
    liq_liq_df["width"] = 1.0
    liq_liq_df["inlet_width"] = 1.0
    liq_liq_df["height"] = 0.48
    liq_liq_df["continuous_flow"] = continuous_flow
    liq_liq_df["gutter_flow"] = gutter_flow

    liq_liq_df["epsilon"] = 0.01 * liq_liq_df["width"]
    liq_liq_df["flow_ratio"] = (
        liq_liq_df["dispersed_flow"] / liq_liq_df["continuous_flow"]
    )
    liq_liq_df["width_ratio"] = round(
        liq_liq_df["inlet_width"] / liq_liq_df["width"], 2
    )
    liq_liq_df["width_ratio"] = liq_liq_df["width_ratio"].astype(str)
    liq_liq_df["type"] = "droplets"

    vol_df = pd.concat([vol_df, liq_liq_df])

    vol_df["fill_vol"] = vol_df.apply(
        lambda row: calc_nondim_fill_volume(row.height, row.width, row.inlet_width),
        axis=1,
    )
    vol_df["squeeze_vol"] = vol_df.apply(
        lambda row: calc_nondim_squeeze_volume(
            row.height,
            row.width,
            row.inlet_width,
            row.epsilon,
            row.continuous_flow,
            row.dispersed_flow,
            row.gutter_flow,
        ),
        axis=1,
    )
    vol_df["vol"] = vol_df["fill_vol"] + vol_df["squeeze_vol"]

    plot = (
        p9.ggplot(
            vol_df, p9.aes("flow_ratio", "vol", color="width_ratio", linetype="type")
        )
        + p9.geom_line()
        + p9.scale_color_manual(color_mapping)
        + p9.ylim(0, 25)
        + p9.scale_x_continuous(breaks=[0, 2, 4, 6, 8, 10])
        + p9.theme_light()
        + p9.labs(
            x="Flow rate ratio (disp. / cont.)",
            y="Dimensionless volume",
            color="w_in / w",
            linetype="Type",
        )
    )

    return plot


# -------------------------------------------------------------------------------------
def make_fig_6(color_mapping: dict[str, str]) -> p9.ggplot:
    """
    Generate figure 6: receding interface during squeezing period

    Arguments:
    `color_mapping`: Dictionary mappying hex colors to width ratios
    """

    width = 100 * 10**-6
    continuous_flow = 3 * 10**-9
    height = 33 * 10**-6
    pinch_thresh = height / (height + width)

    inlet_width_ratios = [1 / 3, 1, 3]
    alpha_vals = list(map(lambda x: float(x / 100), range(0, 1001)))

    inlet_width_col = []
    alpha_col = []
    for inlet_width_ratio, alpha_val in itertools.product(
        inlet_width_ratios, alpha_vals
    ):
        inlet_width_col.append(inlet_width_ratio * width)
        alpha_col.append(alpha_val)

    df = pd.DataFrame()
    df["alpha"] = alpha_col
    df["inlet_width"] = inlet_width_col
    df["width"] = width
    df["height"] = height
    df["continuous_flow"] = continuous_flow

    df["time"] = df["alpha"] / (
        df["continuous_flow"] / (df["height"] * df["width"] ** 2)
    )
    df["epsilon"] = 0.1 * df["width"]
    df["width_ratio"] = round(df["inlet_width"] / df["width"], 2)
    df["width_ratio"] = df["width_ratio"].astype(str)
    df["gutter_flow"] = 0.1 * df["continuous_flow"]
    df["2r"] = df.apply(
        lambda row: calc_2r(
            row.height,
            row.width,
            row.inlet_width,
            row.epsilon,
            row.continuous_flow,
            row.gutter_flow,
            row.time,
        ),
        axis=1,
    )
    df["2r_w"] = df["2r"] / df["width"]

    plot = (
        p9.ggplot(df, p9.aes(x="alpha", y="2r_w", color="width_ratio"))
        + p9.geom_hline(
            p9.aes(yintercept=pinch_thresh), linetype="dashed", color="gray"
        )
        + p9.geom_line()
        + p9.scale_color_manual(color_mapping)
        + p9.scale_y_continuous(
            breaks=[tick / 10 for tick in list(range(0, 14, 2))], limits=[0, 1.2]
        )
        + p9.scale_x_continuous(breaks=[0, 2, 4, 6, 8, 10])
        + p9.theme_light()
        + p9.labs(x="(q_c/(h*w^2))*t", y="2r/w", color="w_in / w")
    )

    return plot


# -------------------------------------------------------------------------------------
def main() -> None:
    """Main function"""

    args = get_args()
    out_dir = args.out_dir

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    color_mapping = {
        "0.33": "#10f900",
        "0.67": "#21cd12",
        "1.0": "#25a918",
        "1.33": "#268b19",
        "2.0": "#246e18",
        "3.0": "#1f4f16",
    }

    fig_2a = make_fig_2a(color_mapping)
    fig_2b = make_fig_2b(color_mapping)
    fig_3 = make_fig_3(color_mapping)
    fig_6 = make_fig_6(color_mapping)

    fig_2a.save(os.path.join(out_dir, "fig_2a.png"))
    fig_2b.save(os.path.join(out_dir, "fig_2b.png"))
    fig_3.save(os.path.join(out_dir, "fig_3.png"))
    fig_6.save(os.path.join(out_dir, "fig_6.png"))


# -------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
