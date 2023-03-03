# Tests

This directory contains the unit and integration tests for the source code in this project.

```sh
.
├── test_filling.py       # Filling module tests
├── test_make_figures.py  # Figure making script integration test
├── test_squeezing.py     # Squeezing module tests
└── test_total.py         # Total module tests
```

# Files

## `test_filling.py`

Unit tests for the functions in module corresponding to the filling phase of droplet formation.

## `test_make_figures.py`

Integration test for the script that makes the replicated figures. The tests ensure that the script can be executed, that it returns a help message for the `-h|--help` flag, and that it generates the figures when run.

## `test_squeezing.py`

Unit tests for the functions in module corresponding to the squeezing phase of droplet formation.

## `test_total.py`

Unit tests for the functions in module which combines the filling and squeezing phase contributions to total volume.
