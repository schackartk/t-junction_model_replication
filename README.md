# [Re] Predictive model for the size of bubbles and droplets created in microfluidic T-junctions

![Tests Status](./.reports/tests/tests_badge.svg?dummy=8484744)
![Total Coverage](./.reports/coverage/coverage_all_badge.svg?dummy=8484744)
![Module Coverage](./.reports/coverage/coverage_modules_badge.svg?dummy=8484744)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-360/)
![Flake8](./.reports/flake8/flake8_badge.svg?dummy=8484744)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
![mypy](https://img.shields.io/badge/%20type_checker-mypy-%231674b1?style=flat)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://github.com/psf/black"><img alt="MIT License" src="https://img.shields.io/github/license/schackartk/t-junction_model_replication"></a>

This repository contains the code used to replicate the mathematical modeling results found in van Steijn V., *et al.* 2010 for submission to ReScience C.

# Repository Structure

The following is a brief overview of the contents of this respository:

```sh
.
├── .reports/        # Static code check reports & badges
├── LICENSE          # License file
├── Makefile         # Make commands
├── article/         # Article (LaTeX) contents
├── environment.yml  # Conda environment description
├── figures/         # Replicated figures
├── requirements.txt # pip requirements
├── setup.cfg        # Code check configurations
├── src/             # Code
└── tests/           # Integration tests
```

# Systems

The code for this project was developed using [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) connected to an [Ubuntu 20.04](https://releases.ubuntu.com/focal/) kernel. Compatibility to other systems may vary. In particular, certain functionality (like GNU Make) may not work on Windows.

If you would like to run the code on a Windows machine, we recommend using WSL2. [This protocol](https://www.protocols.io/view/install-wsl-and-vscode-on-windows-10-q26g78e1klwz/v1) may be helpful for getting that set up.

# Installation

## Cloning

First, clone the repository to your system locally. From the command-line in the directory where you would like to clone the project, run:

```sh
# If you have ssh keys set up
$ git clone git@github.com:schackartk/t-junction_model_replication.git

# If you do not have ssh keys set up
$ git clone https://github.com/schackartk/t-junction_model_replication.git
```

Then change directory into the project:

```sh
$ cd t-junction_model_replication/
```

## Dependencies

We provide two options for installing the dependencies of this project, `conda` and `pip`.

### `conda`

If you have conda installed, you can create a conda environment using the provided `environment.yml` by running:

```
$ conda env create -f environment.yml -p ./env
```

This creates a conda environment in the root of the repository, which is activated with:

```sh
$ conda activate ./env
```

### `pip`

Alternatively, pip can be used. This project was developed with Python 3.11.0, so it is best to ensure that version is installed.

To see if Python 3.11 is available, run:
```sh
$ which python3.11
```

If this returns a python3.11 path, skip this next step.
If nothing is returned, install Python 3.11:
```sh
$ sudo apt update
$ sudo apt install python3.11
```

We also recommend using a virtual environment. To get the package `venv` for Python3.11, run:

```sh
$ sudo apt install python3.11-venv
```

Then create a virtual environment. For example, you may call in `env`:

```sh
$ python3.11 -m venv env
```

And activate it:

```sh
$ source ./env/bin/activate
```

Then pip can be used to install the requirements (preferably in a virtual environment as described above):

```
$ pip install -r requirements.txt
```

# Testing

The code in this repository was developed using various code tests and static checks. Flake8 and pylint are used for static code checking, and mypy is used for static type checking. Pytest is used as a testing framework to support unit tests.

The full test suite can be run with the following command:

```
$ make test
```

All tests have passed during development, any failing tests may be indicative of issues with environment/packages.

# Replicating results

To generate the figures and output them to `figures/` (the default), run:

```
$ src/make_figures.py
Generating figures...
Saving figures...
Done. See figures in "figures".
```

*Note*: if you are not running the code in a virtual or conda environment, your system may default to using an incorrect Python version leading to errors. If this is the case, specify the Python version when running, for example:

```sh
$ python3.11 src/make_figures.py
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
```

# Authorship

Kenneth E. Schackart III: (Formerly) University of Arizona, Tucson Arizona, United States of America

Kattika Kaarj: Suranaree University of Technology, Nakhon Ratchasima, Thailand 
