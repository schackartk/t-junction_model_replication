#!/usr/bin/env python

"""
Author : Kenneth Schackart <schackartk1@gmail.com>
Date   : 2023-02-04
Purpose: Test figure genertating script
"""

import os
import random
import shutil
import string
from subprocess import getstatusoutput

PRG = "src/make_figures.py"


# -------------------------------------------------------------------------------------
def random_string() -> str:
    """Generate a random string"""

    return "".join(random.choices(string.ascii_uppercase + string.digits, k=5))


# -------------------------------------------------------------------------------------
def test_exists() -> None:
    """Program exists"""

    assert os.path.isfile(PRG)


# -------------------------------------------------------------------------------------
def test_usage() -> None:
    """Usage"""

    for flag in ["-h", "--help"]:
        retval, out = getstatusoutput(f"{PRG} {flag}")
        assert retval == 0
        assert out.lower().startswith("usage")


# -------------------------------------------------------------------------------------
def test_runs_okay() -> None:
    """Runs on good input"""

    out_dir = random_string()
    out_file_names = ["fig_2a.png", "fig_2a_incorrect.png", "fig_2b.png", "fig_3.png", "fig_6.png"]

    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        rv, _ = getstatusoutput(f"{PRG} -o {out_dir}")

        assert rv == 0
        out_files = [os.path.join(out_dir, filename) for filename in out_file_names]
        assert os.path.isdir(out_dir)
        for out_file in out_files:
            assert os.path.isfile(out_file)

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)
