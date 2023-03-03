# T-junction Modules

This directory contains modules used to model T-junction droplet/bubble formation. The modules are divided into those used during the filling and squeezing phases, and a module for combining those two contributions.

```sh
.
├── __init__.py            # Allow modules to be imported
├── filling.py             # Filling phase module
├── squeezing.py           # Squeezing phase module
├── total.py               # Total volume prediction module
└── tests/                 # Module unit tests
    ├── test_filling.py    # Filling module tests
    ├── test_squeezing.py  # Squeezing module tests
    └── test_total.py      # Total module tests
```
# Files

## `__init__.py`

This file simply allows the Python modules to be imported by other modules/scripts.


## `filling.py`

Module that contains functions that model the filling phase of droplet/bubble formation.

When using the functions in this module, use consistent units to ensure consistent and accurate outputs. We recommend using only SI units (*e.g.* m, L; not µm, mL, *etc.*) to avoid inconsistencies.

## `squeezing.py`

Module that contains functions that model the squeezing phase of droplet/bubble formation.

When using the functions in this module, use consistent units to ensure consistent and accurate outputs. We recommend using only SI units (*e.g.* m, L; not µm, mL, *etc.*) to avoid inconsistencies.

## `total.py`

Module that combines the contributions from squeezing and filling phases to calculate the total predicted volume.

# `tests/`

The tests directory contains Python files containing the unit tests for the functions defined in the modules.
