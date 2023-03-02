# T-Junction Code

This directory contains code used for replicating the figures modelling the formation of droplets and bubbles in microfuilic T-junctions.

```sh
.
├── utils/           # Modules and utilities
└── make_figures.py  # Script for replicating figures
```

## `utils/`

This directory contains the utilities used in this project. The majority of this constists of Python modules.

These modules are ideal for reuse of the developed mathematical model. While `make_figures.py` strictly regenerates the figures in the original work, these modules can be used more generally to apply the model.

## `make_figures.py`

The script `src/make_figures.py` can be executed to generate the figures which replicate those in the original work.

This script imports several functions from the modules within `utils/`. Only the mathematical modeling portions of the figures in the original work are replicated, not plotting of empirical data.

Help for this script can be accessed with `-h|--help`:

```
$ src/make_figures.py -h
usage: make_figures.py [-h] [-o DIR]

Create figures which replicate those in the original work using the modules developed in this project.

options:
  -h, --help         show this help message and exit
  -o, --out-dir DIR  Output directory (default: figures/)
```

By default all figures are output to `figures/`. However, this can be changed using the optional `-o|--out-dir` flag.

For example, to generate the figures and output them to `new_figures/`, run:

```
$ src/make_figures.py -o new_figures/
Generating figures...
Saving figures...
Done. See figures in "new_figures".
```

This will create five figures in the output directory:

```sh
$ ls new_figures/
fig_2a.png  fig_2a_incorrect.png  fig_2b.png  fig_3.png  fig_6.png
```