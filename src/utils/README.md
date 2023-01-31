# T-Junction Modules and Utilities

This directory contains modules used to mode T-Junction flow. The modules are divided into those used during the filling and squeezing phases.

```sh
.
├── __init__.py            # Allow modules to be imported
├── center.sh              # Output formatting for Make targets
├── filling.py             # Filling phase module
└── squeezing.py           # Squeezing phase module
```
# Files

## `__init__.py`

This file simply allows the Python modules to be imported by other modules/scripts.

## `center.sh`

Shell script that prints a string fenced by "=" to the edges of the terminal. For example:

```sh
===================== Running Pytest =====================
```

It is used for formatting output of the Make targets.

## `filling.py`

Module that contains functions that model the filling phase of droplet/bubble formation.

## `squeezing.py`

Module that contains functions that model the squeezing phase of droplet/bubble formation.
