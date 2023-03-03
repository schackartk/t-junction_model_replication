# Source code

This directory contains code used for replicating the figures modelling the formation of droplets and bubbles in microfuilic T-junctions.

```sh
.
├── t_junction_model/           # Python modules
├── tests/                      # Unit and integration tests
├── utils/                      # Project utilities
└── make_figures.py             # Script for replicating figures
```

## `t_junction_model/`

This directory contains the Python modules used in this project.

These modules are ideal for reuse of the developed mathematical model. While `make_figures.py` strictly regenerates the figures in the original work, these modules can be used more generally to apply the model.

## `tests/`

This directory contains the unit and integration tests for the source code in this project.

## `utils/`

This directory contains utilities used in this project that are not directly related to modeling T-junction droplet/bubble formation.

## `make_figures.py`

The script `make_figures.py` can be executed to generate the figures which replicate those in the original work.

This script imports several functions from the modules within `module/`. Only the mathematical modeling portions of the figures in the original work are replicated, not plotting of empirical data.

Help for this script can be accessed with `-h|--help`:

```
$ ./make_figures.py -h
usage: make_figures.py [-h] [-o DIR]

Create figures which replicate those in the original work using the modules developed in this project.

options:
  -h, --help         show this help message and exit
  -o, --out-dir DIR  Output directory (default: out/)
```

By default all figures are output to `out/`. However, this can be changed using the optional `-o|--out-dir` flag.

For example, to generate the figures and output them to `../new_figures/`, run:

```
$ ./make_figures.py -o ../new_figures/
Generating figures...
Saving figures...
Done. See figures in "../new_figures/".
```

This will create five figures in the output directory:

```sh
$ ls ../new_figures/
fig_2a.png  fig_2a_incorrect.png  fig_2b.png  fig_3.png  fig_6.png
```