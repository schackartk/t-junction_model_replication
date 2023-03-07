#!/usr/bin/env python3
"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2023-01-29
Purpose: Generate figures from van Steijn et al., (https://doi.org/10.1039/c002625e)
"""

import argparse
import itertools
import os
from typing import Callable, NamedTuple

import pandas as pd
import plotnine as p9

from t_junction_model.filling import (
    calc_incorrect_nondim_fill_volume,
    calc_nondim_fill_volume,
)
from t_junction_model.squeezing import _calc_2r, _calc_alpha
from t_junction_model.total import calc_nondim_total_volume
from formatters.formatter_class import CustomHelpFormatter

# Dictionary mapping inlet width / channel with ratio to color
COLOR_MAPPING = {
    "0.33": "#CF232B",
    "0.67": "#CF232B",
    "1.0": "#CF232B",
    "1.33": "#CF232B",
    "2.0": "#CF232B",
    "3.0": "#CF232B",
}


class Args(NamedTuple):
    """Command-line arguments"""

    out_dir: str


# -------------------------------------------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description=(
            "Create figures which replicate those in the original work"
            " using the modules developed in this project."
        ),
        formatter_class=CustomHelpFormatter,
    )

    parser.add_argument(
        "-o",
        "--out-dir",
        help="Output directory",
        metavar="DIR",
        type=str,
        default="out/",
    )

    args = parser.parse_args()

    return Args(args.out_dir)


# -------------------------------------------------------------------------------------
def make_fig_2a(color_mapping: dict[str, str], filling_function: Callable) -> p9.ggplot:
    """
    Generate figure 2a: nondimensionalized volume during the filling phase
    plotted against channel height/width for 5 inlet width/width ratios

    Arguments:
    `color_mapping`: Dictionary mapping hex colors to width ratios
    `filling_function`: Function to use for calculating nondimensionalized
    filling volume (either t_junction_model.filling.calc_nondim_fill_volume
    or t_junction_model.filling.calc_incorrect_nondim_fill_volume)
    """

    widths = [1.0]
    heights = map(lambda x: float(x / 2000), range(1, 1001))
    inlet_widths = [1, 4 / 3, 2, 3]

    width_col = []
    height_col = []
    inlet_width_col = []
    for width, height, inlet_width in itertools.product(widths, heights, inlet_widths):
        width_col.append(width)
        height_col.append(height)
        inlet_width_col.append(inlet_width)

    df = pd.DataFrame()
    df["width"] = width_col
    df["height"] = height_col
    df["inlet_width"] = inlet_width_col

    df["height_over_width"] = df["height"] / df["width"]
    df["width_ratio"] = round(df["inlet_width"] / df["width"], 2)
    df["width_ratio"] = df["width_ratio"].astype(str)
    df["width_ratio_labs"] = df.apply(lambda row: "w_in/w=" + row.width_ratio, axis=1)

    df["nondim_vol"] = df.apply(
        lambda row: filling_function(row.height, row.width, row.inlet_width),
        axis=1,
    )

    plot = (
        p9.ggplot(
            df,
            p9.aes("height_over_width", "nondim_vol", color="width_ratio"),
        )
        + p9.geom_line()
        + p9.scale_color_manual(color_mapping)
        + p9.geom_label(
            df[df["height_over_width"] == 0.25],
            p9.aes(
                label="width_ratio_labs",
            ),
            size=8,
            color="black",
            label_size=0,
        )
        + p9.scale_y_continuous(
            breaks=[tick / 10 for tick in list(range(0, 22, 2))], limits=[0, 2]
        )
        + p9.theme_light()
        + p9.labs(x="h/w", y="Dimensionless fill volume")
        + p9.theme(legend_position="none")
    )

    return plot


# -------------------------------------------------------------------------------------
def make_fig_2b(color_mapping: dict[str, str]) -> p9.ggplot:
    """
    Generate figure 2b: squeezing coefficient alpha
    plotted against channel height/width for 5 inlet width/width ratios

    Arguments:
    `color_mapping`: Dictionary mapping hex colors to width ratios
    """

    widths = [1.0]
    flow_ratio = 0.1
    corner_roundness = 0.0
    heights = map(lambda x: float(x / 2000), range(1, 1001))
    inlet_widths = [1 / 3, 2 / 3, 1, 4 / 3, 2, 3]

    width_col = []
    height_col = []
    inlet_width_col = []
    for width, height, inlet_width in itertools.product(widths, heights, inlet_widths):
        width_col.append(width)
        height_col.append(height)
        inlet_width_col.append(inlet_width)

    df = pd.DataFrame()
    df["width"] = width_col
    df["height"] = height_col
    df["inlet_width"] = inlet_width_col
    df["corner_roundness"] = corner_roundness
    df["flow_cont"] = 1.0
    df["flow_gutter"] = df["flow_cont"] * flow_ratio

    df["height_over_width"] = df["height"] / df["width"]
    df["width_ratio"] = round(df["inlet_width"] / df["width"], 2)
    df["width_ratio"] = df["width_ratio"].astype(str)
    df["width_ratio_labs"] = df.apply(lambda row: "w_in/w=" + row.width_ratio, axis=1)

    df["alpha"] = df.apply(
        lambda row: _calc_alpha(
            row.height,
            row.width,
            row.inlet_width,
            row.corner_roundness,
            row.flow_cont,
            row.flow_gutter,
        ),
        axis=1,
    )

    plot = (
        p9.ggplot(df, p9.aes("height_over_width", "alpha", color="width_ratio"))
        + p9.geom_line()
        + p9.scale_y_continuous(breaks=list(range(0, 9, 1)), limits=[0, 8])
        + p9.scale_color_manual(color_mapping)
        + p9.geom_label(
            df[df["height_over_width"] == 0.25],
            p9.aes(
                label="width_ratio_labs",
            ),
            size=8,
            color="black",
            label_size=0,
        )
        + p9.theme_light()
        + p9.labs(x="h/w", y="Squeezing coefficient")
        + p9.theme(legend_position="none")
    )

    return plot


# -------------------------------------------------------------------------------------
def make_fig_3(color_mapping: dict[str, str]) -> p9.ggplot:
    """
    Generate figure 3: dimensionless volume of bubbles and droplets
    against flow rate ratio for 5 width ratios

    Arguments:
    `color_mapping`: Dictionary mapping hex colors to width ratios
    """

    continuous_flow = 1.0
    gutter_flow = continuous_flow * 0.1
    width = 1.0
    inlet_widths = [1 / 3, 2 / 3, 1, 4 / 3, 3]
    dispersed_flows = list(map(lambda x: float(x / 100), range(1, 1001)))

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
    df = pd.DataFrame()
    df["inlet_width"] = inlet_width_col
    df["dispersed_flow"] = dispersed_flow_col
    df["width"] = width
    df["continuous_flow"] = continuous_flow
    df["gutter_flow"] = gutter_flow
    df["type"] = "bubbles"

    df["corner_roundness"] = 0.1 * df["width"]
    df["flow_ratio"] = df["dispersed_flow"] / df["continuous_flow"]
    df["width_ratio"] = round(df["inlet_width"] / df["width"], 2)
    df["width_ratio"] = df["width_ratio"].astype(str)
    df["height"] = df.apply(lambda row: height_dictionary.get(row.width_ratio), axis=1)

    # Parameters for droplets
    liq_liq_df = pd.DataFrame()
    liq_liq_df["dispersed_flow"] = dispersed_flows
    liq_liq_df["width"] = 1.0
    liq_liq_df["inlet_width"] = 1.0
    liq_liq_df["height"] = 0.48
    liq_liq_df["continuous_flow"] = continuous_flow
    liq_liq_df["gutter_flow"] = gutter_flow

    liq_liq_df["corner_roundness"] = 0.01 * liq_liq_df["width"]
    liq_liq_df["flow_ratio"] = (
        liq_liq_df["dispersed_flow"] / liq_liq_df["continuous_flow"]
    )
    liq_liq_df["width_ratio"] = round(
        liq_liq_df["inlet_width"] / liq_liq_df["width"], 2
    )
    liq_liq_df["width_ratio"] = liq_liq_df["width_ratio"].astype(str)
    liq_liq_df["type"] = "droplets"

    df = pd.concat([df, liq_liq_df])

    df["vol"] = df.apply(
        lambda row: calc_nondim_total_volume(
            row.height,
            row.width,
            row.inlet_width,
            row.corner_roundness,
            row.continuous_flow,
            row.dispersed_flow,
            row.gutter_flow,
        ),
        axis=1,
    )
    df["width_ratio_labs"] = df.apply(lambda row: "w_in/w=" + row.width_ratio, axis=1)

    df = df[df["vol"] <= 25]
    label_df = df[df["vol"] <= 25 - 2.5 * (df["flow_ratio"] - 0.009)]
    label_df = label_df[label_df["vol"] >= 25 - 2.5 * (label_df["flow_ratio"] + 0.009)]
    label_df["flow_ratio"][label_df["type"] == "droplets"] = 8
    plot = (
        p9.ggplot(df, p9.aes("flow_ratio", "vol", color="width_ratio", linetype="type"))
        + p9.geom_line()
        + p9.scale_color_manual(color_mapping)
        + p9.ylim(0, 25)
        + p9.scale_x_continuous(breaks=[0, 2, 4, 6, 8, 10])
        + p9.geom_label(
            label_df,
            p9.aes(
                label="width_ratio_labs",
            ),
            size=8,
            color="black",
            label_size=0,
        )
        + p9.annotate(
            "path",
            x=[8, 8],
            y=[11, 13.5],
            arrow=p9.arrow(length=0.075, type="closed", ends="last", angle=20),
        )
        + p9.theme_light()
        + p9.labs(
            x="Flow rate ratio (disp. / cont.)",
            y="Dimensionless volume",
            color="w_in / w",
            linetype="Type",
        )
        + p9.theme(legend_position="none")
    )

    return plot


# -------------------------------------------------------------------------------------
def make_fig_6(color_mapping: dict[str, str]) -> p9.ggplot:
    """
    Generate figure 6: receding interface during squeezing period

    Arguments:
    `color_mapping`: Dictionary mapping hex colors to width ratios
    """

    width = 100 * 10**-6
    continuous_flow = 3 * 10**-9
    height = 33 * 10**-6
    pinch_thresh = height / (height + width)

    inlet_width_ratios = [1 / 3, 1, 3]
    alpha_vals = list(map(lambda x: float(x / 100), range(1, 1001)))

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
    df["corner_roundness"] = 0.1 * df["width"]
    df["width_ratio"] = round(df["inlet_width"] / df["width"], 2)
    df["width_ratio"] = df["width_ratio"].astype(str)
    df["gutter_flow"] = 0.1 * df["continuous_flow"]
    df["2r"] = df.apply(
        lambda row: _calc_2r(
            row.height,
            row.width,
            row.inlet_width,
            row.corner_roundness,
            row.continuous_flow,
            row.gutter_flow,
            row.time,
        ),
        axis=1,
    )
    df["2r_w"] = df["2r"] / df["width"]
    df["width_ratio_labs"] = df.apply(lambda row: "w_in/w=" + row.width_ratio, axis=1)
    lab_df = df[df["2r_w"] >= 0.1 * (df["alpha"] - 0.09) + 0.275]
    lab_df = lab_df[lab_df["2r_w"] <= 0.1 * (lab_df["alpha"] + 0.09) + 0.275]

    y_max = 1.2
    df = df[df["2r_w"] <= y_max]
    df = df[df["2r_w"] >= 0]
    plot = (
        p9.ggplot(df, p9.aes(x="alpha", y="2r_w", color="width_ratio"))
        + p9.geom_hline(
            p9.aes(yintercept=pinch_thresh), linetype="dashed", color="gray"
        )
        + p9.geom_line()
        + p9.scale_color_manual(color_mapping)
        + p9.geom_label(
            lab_df,
            p9.aes(
                label="width_ratio_labs",
            ),
            size=8,
            color="black",
            label_size=0,
        )
        + p9.scale_y_continuous(
            breaks=[tick / 10 for tick in list(range(0, 14, 2))], limits=[0, y_max]
        )
        + p9.annotate(
            "label",
            x=4.5,
            y=pinch_thresh,
            label="2r/w = h/(h+w)",
            size=8,
            label_size=0,
        )
        + p9.scale_x_continuous(breaks=[0, 2, 4, 6, 8, 10])
        + p9.theme_light()
        + p9.labs(x="Dimensionless time", y="2r/w", color="w_in / w")
        + p9.theme(legend_position="none")
    )

    return plot


# -------------------------------------------------------------------------------------
def main() -> None:
    """Main function"""

    args = get_args()
    out_dir = args.out_dir

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    print("Generating figures...")
    fig_2a = make_fig_2a(COLOR_MAPPING, calc_nondim_fill_volume)
    fig_2a_incorrect = make_fig_2a(COLOR_MAPPING, calc_incorrect_nondim_fill_volume)
    fig_2b = make_fig_2b(COLOR_MAPPING)
    fig_3 = make_fig_3(COLOR_MAPPING)
    fig_6 = make_fig_6(COLOR_MAPPING)

    print("Saving figures...")
    fig_2a.save(
        os.path.join(out_dir, "fig_2a.png"), width=6.4, height=4.8, verbose=False
    )
    fig_2a_incorrect.save(
        os.path.join(out_dir, "fig_2a_incorrect.png"),
        width=6.4,
        height=4.8,
        verbose=False,
    )
    fig_2b.save(
        os.path.join(out_dir, "fig_2b.png"), width=6.4, height=4.8, verbose=False
    )
    fig_3.save(os.path.join(out_dir, "fig_3.png"), width=6.4, height=4.8, verbose=False)
    fig_6.save(os.path.join(out_dir, "fig_6.png"), width=6.4, height=4.8, verbose=False)

    print(f'Done. See figures in "{out_dir}".')


# -------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
