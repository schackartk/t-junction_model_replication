# Formatters

This directory contains a shell script and Python module, both of which are used for formatting outputs to the terminal.

```sh
.
├── __init__.py            # Allow modules to be imported
├── center.sh              # Output formatting for Make targets
└── formatter_class.py     # Argparse help formatter
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

## `formatter_class.py`

Custom Python argparse help formatter class.
