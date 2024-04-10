# climplots

This Python project is able to plot absolute values and anomalies
from CSV and netCDF files containing timeseries data. Moreover, the
computed data can be saved in a new netCDF file. For usage
information, type `climplots --help`.

Usage of the Python project:
 
```
climplots [-h] --input-file INPUT_FILE [--latitude-range LAT_MIN LAT_MAX]
          [--timeseries] [--anomalies] [--trend] [--output-file OUTPUT_FILE]
```


## Installation

Use the following command in the base directory to install:

```bash
python -m pip install .
```

For an editable ("developer mode") installation, use the following
instead:

```bash
python -m pip install -e .
```

With this, the installation is actually a link to the original source code,
i.e. each change in the source code is immediately available.


## Prerequisites

You need a working Python environment, and `pip` installed.

E.g., with `conda`:

```bash
conda create --name mynewenv python
conda activate mynewenv
python -m pip install -e .
```


## Notes

Python packaging is evolving towards new packaging tools. This example project is using
the "old" way of doing packaging, due to its relative simplicity, and because the
transition to the "new" way is still ongoing. For the future, please be aware that
Python packages should contain a `pyproject.toml` file containing all relevant
information needed for building and deploying a project. There are several tools
already available dealing with the "new" way, most prominently maybe `poetry`.

If you are about to start a new project of your own, do have a look at `poetry`.

Some relevant links:

- pep-517: https://www.python.org/dev/peps/pep-0517/
- pep-621: https://www.python.org/dev/peps/pep-0621/
- https://python-poetry.org/
- https://cjolowicz.github.io/posts/hypermodern-python-01-setup/
