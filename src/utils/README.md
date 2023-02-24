# T-Junction Modules and Utilities

This directory contains modules used to mode T-Junction flow. The modules are divided into those used during the filling and squeezing phases.

```sh
.
├── __init__.py            # Allow modules to be imported
├── center.sh              # Output formatting for Make targets
├── filling.py             # Filling phase module
├── formatter_class.py     # Argparse help formatter
└── squeezing.py           # Squeezing phase module
```
# Files

## `__init__.py`

This file simply allows the Python modules to be imported by other modules/scripts.

## `center.sh`

Shell script that prints a string fenced by "=" to the edges of the terminal. For example:

```sh
$ ./center.sh "Running Pytest"
===================== Running Pytest =====================
```

It is used for formatting output of the Make targets.

## `filling.py`

Module that contains functions that model the filling phase of droplet/bubble formation.

When using the functions in this module, use consistent units to ensure consistent and accurate outputs. We recommend using only SI units (*e.g.* m, L; not µm, mL, *etc.*) to avoid inconsistencies.

## `formatter_class.py`

Custom Python argparse help formatter class.

## `squeezing.py`

Module that contains functions that model the squeezing phase of droplet/bubble formation.

When using the functions in this module, use consistent units to ensure consistent and accurate outputs. We recommend using only SI units (*e.g.* m, L; not µm, mL, *etc.*) to avoid inconsistencies.
