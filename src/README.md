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

This script can be executed to generate the figures which replicate those in the original work.

This script imports several functions from the modules within `utils/`. Only the mathematical modeling portions of the figures in the original work are replicated, not plotting of empirical data.

By default all figures are output to `figures/`. However, this can be changed using the optional `-o|--out-dir` flag.

To generate the figures and output them to `figures/` (the default), run:

```
$ src/make_figures.py
Generating figures...
Saving figures...
Done. See figures in "new_figures".
```

This will create five figures in the output directory. The names of the figures correspond to the figure numbers in the original work.

```sh
$ tree figures/
figures/
├── fig_2a.png             # Figure 2a using correct eqn
├── fig_2a_incorrect.png   # Figure 2a as shown in original work
├── fig_2b.png             # Figure 2b as shown in original work
├── fig_3.png              # Figure 3 as shown in original work
└── fig_6.png              # Figure 6 as shown in original work
``
