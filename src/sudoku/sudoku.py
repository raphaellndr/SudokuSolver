"""Module defining a sudoku."""

import random
from pathlib import Path

import numpy as np
from numpy import typing as npt

from .backtracking import backtracking
from .exceptions import ConsistencyError
from .grid import Grid


class Sudoku:
    """Defines a sudoku."""

    def __init__(self, file_path: str | Path | None = None) -> None:
        if file_path is not None:
            if isinstance(file_path, str):
                self.file_path = Path(file_path)
            else:
                self.file_path = file_path
            self._values = self._get_values()
        else:
            self._values = np.zeros((9, 9), dtype=np.uint8)
        self._grid = Grid(self._values)

    @property
    def grid(self) -> Grid:
        """Returns grid containing the sudoku."""
        return self._grid

    def _get_values(self) -> npt.NDArray[np.uint8]:
        """Gets values contained in raw file.

        Each dot is converted to a 0.

        :returns: `np.ndarray` containing converted values.
        """
        with open(self.file_path, encoding="utf-8") as stream:
            lines = [line.strip() for line in stream.readlines()]
        array = np.array(
            [[int(c) if c != "." else 0 for c in line] for _, line in enumerate(lines)],
            dtype=np.uint8,
        )
        return array

    def _save_to_file(self, file_path: Path) -> None:
        """Saves the sudoku grid to a file in the specified format.

        :param file_path: path to the file where the sudoku grid will be saved.
        """
        with open(file_path, "w", encoding="utf-8") as file:
            for row in range(9):
                line = ""
                for col in range(9):
                    value = self._values[row, col]
                    line += str(value) if value != 0 else "."
                file.write(line + "\n")

    def solve(self) -> None:
        """Calls backtracking algorithm to solve the sudoku."""
        backtracking(
            grid=self.grid,
            domains=self.grid.domains,
            initial_domains=self.grid.initial_domains,
        )

    def generate(self, *, difficulty: str, destination_path: str) -> None:
        """Generates a Sudoku puzzle with specified difficulty and saves it to a file.

        This method uses the backtracking algorithm to generate a Sudoku puzzle with a unique
        solution. (uniqueness not yet implemented)
        The generated puzzle is then saved to the specified file in the following format:

        6.5.4213.
        .2.13..7.
        1....6...
        3..7.....
        ......8..
        ......24.
        ..1.2....
        .....7..4
        4..3..5.8

        :param difficulty: the difficulty level of the generated Sudoku puzzle. Options are "easy",
        "medium", or "hard".
        :param destination_path: path to the file where the generated Sudoku puzzle will be saved.
        """
        backtracking(
            grid=self.grid,
            domains=self.grid.domains,
            initial_domains=self.grid.initial_domains,
            mode="generate",
        )

        match difficulty:
            case "easy":
                cells_to_remove = random.randint(25, 30)
            case "medium":
                cells_to_remove = random.randint(35, 40)
            case "hard":
                cells_to_remove = random.randint(45, 50)
            case _:
                raise ValueError(f"Unknown difficulty '{difficulty}'")

        for _ in range(cells_to_remove):
            row, col = np.random.randint(9, size=2)
            while self.grid.get_value((row, col)) == 0:
                row, col = np.random.randint(9, size=2)
            self.grid.domains.reinitialize_domain(
                domain_index=(row, col), initial_domains=self.grid.initial_domains
            )
            self.grid.reinitialize_value((row, col))

        self._save_to_file(Path(destination_path))

    def check_consistency(self) -> bool:
        """Checks the consistency of the sudoku.

        :returns: `True` if the sudoku is consistent, `False` otherwise.
        :raises: `ConsistencyError` if sudoku is inconsistent.
        """
        for index in self.grid.assigned_values_indexes:
            value = self.grid.get_value(index)
            if not self.grid.check_constraints(value=value, value_index=index):
                raise ConsistencyError(file_path=self.file_path, value_index=index)  # type:ignore
        return True

    def humanize(self) -> str:
        """Renders the grid in a more readable way.

        :returns: formatted sudoku.
        """
        formatted_sudoku = ""
        for i, row in enumerate(self._values):
            if i % 3 == 0 and i != 0:
                formatted_sudoku += "-" * 21 + "\n"
            formatted_sudoku += (
                " ".join(map(str, row[:3]))
                + " | "
                + " ".join(map(str, row[3:6]))
                + " | "
                + " ".join(map(str, row[6:]))
                + "\n"
            )

        return formatted_sudoku
