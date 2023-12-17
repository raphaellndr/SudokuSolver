# Sudoku

## Installation instructions

### Prerequisites

First, [poetry](https://github.com/python-poetry/poetry) needs to be installed on your machine. If 
not, simply head to the [documentation](https://python-poetry.org/docs/#installation) and follow the 
instructions.

### Installation

Once poetry correctly installed, do as follows to set up your project:

- Head to your project:
```shell
cd sudoku
```

- Spawn a shell, within the virtual environment (if one doesn’t exist yet, it will be created):
```shell
poetry shell
```

- Lock (without installing) the dependencies specified in pyproject.toml:
```shell
poetry lock
```

- Read the pyproject.toml file from the current project, resolve the dependencies and install them:
```shell
poetry install
```
