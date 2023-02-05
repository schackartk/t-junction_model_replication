# [Re] Predictive model for the size of bubbles and droplets created in microfluidic T-junctions

This repository contains the code used to replicate the mathematical modelling results found in van Steijn V., *et al.* 2010 for submission to ReScienceC

# Repository Structure

The following is a brief overview of the contents of this respository:

```sh
.
├── LICENSE          # License file
├── Makefile         # Make commands
├── article/         # Article (LaTeX) contents
├── environment.yml  # Conda environment description
├── figures/         # Replicated figures
├── requirements.txt # pip requirements
├── setup.cfg        # Code check configurations
├── src/             # Code
└── tests            # Integration tests
```

# Setup

We provide two options for installing the dependencies of this project.

## `conda`

To create a conda environment using the provided `environment.yml`, the following can be run:

```
$ conda env create -f environment.yml -p ./env
```

This creates a conda environment in the root of the repository, which is activated with:

```sh
$ conda activate ./env
```

## `pip`

Alternatively, pip can be used. This project was developed with Python 3.11.0, so it is best to ensure that version is installed.

The following can be executed (preferably in an isolated or virtual environment) to install with pip:

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

The script `src/make_figures.py` is used to generate the replicated figures. Help for that script can be accessed with `-h|--help`:

```sh
$ src/make_figures.py -h
```

By default all figures are output to `figures/`. However, this can be changed using the optional `-o|--out-dir` flag.

# Authorship

Kenneth E. Schackart III: Research Software Consulting, Tucson Arizona, United States of America

Kattika Kaarj: Suranaree University of Technology, Nakhon Ratchasima, Thailand 