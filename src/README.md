# T-Junction Code

This directory contains code  used for replicating the figures modelling T-Junction flow.

```sh
.
├── utils/           # Modules and utilities
└── make_figures.py  # Script for replicating figures
```

## `utils/`

This directory contains the utilities used in this project. The majority of this constists of Python modules.

These modules are ideal for reuse of the developed matheematical model. While `make_figures.py` strictly regenerates the figures in the original work, these modules can be used more generally to apply the model.

## `make_figures.py`

This script can be executed to generate the figures which replicate those in the original work.

This script imports several functions from the modules within `utils/`. Only the mathematical modeling portions of the figures in the original work are replicated, not plotting of empirical data.

