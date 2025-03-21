"""Sudoku tests module."""

import numpy as np
import pytest

from sudoku_resolver.exceptions import ConsistencyError
from sudoku_resolver.sudoku import Sudoku
from tests import SUDOKU_PATH


def test_initialize_values() -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)

    assert (
        sudoku.grid._values
        == np.asarray(
            [
                [6, 0, 5, 0, 4, 2, 1, 3, 0],
                [0, 2, 0, 1, 3, 0, 0, 7, 0],
                [1, 0, 0, 0, 0, 6, 0, 0, 0],
                [3, 0, 0, 7, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 8, 0, 0],
                [0, 0, 0, 0, 0, 0, 2, 4, 0],
                [0, 0, 1, 0, 2, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 7, 0, 0, 4],
                [4, 0, 0, 3, 0, 0, 5, 0, 8],
            ],
            dtype=np.uint8,
        )
    ).all()


def test_solve_sudoku() -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)
    sudoku.solve()

    assert (
        sudoku.grid._values
        == np.asarray(
            [
                [6, 7, 5, 8, 4, 2, 1, 3, 9],
                [8, 2, 4, 1, 3, 9, 6, 7, 5],
                [1, 9, 3, 5, 7, 6, 4, 8, 2],
                [3, 5, 2, 7, 8, 4, 9, 6, 1],
                [9, 4, 6, 2, 1, 3, 8, 5, 7],
                [7, 1, 8, 9, 6, 5, 2, 4, 3],
                [5, 3, 1, 4, 2, 8, 7, 9, 6],
                [2, 8, 9, 6, 5, 7, 3, 1, 4],
                [4, 6, 7, 3, 9, 1, 5, 2, 8],
            ],
            dtype=np.uint8,
        )
    ).all()


def test_check_consistency() -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)
    sudoku.solve()

    assert sudoku.check_consistency()


def test_check_inconsistency() -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)
    sudoku.solve()
    sudoku.grid._values[0][0] = 1

    with pytest.raises(ConsistencyError):
        sudoku.check_consistency()


def test_humanize() -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)
    sudoku.solve()

    assert (
        sudoku.humanize() == "6 7 5 | 8 4 2 | 1 3 9\n"
        "8 2 4 | 1 3 9 | 6 7 5\n"
        "1 9 3 | 5 7 6 | 4 8 2\n"
        "---------------------\n"
        "3 5 2 | 7 8 4 | 9 6 1\n"
        "9 4 6 | 2 1 3 | 8 5 7\n"
        "7 1 8 | 9 6 5 | 2 4 3\n"
        "---------------------\n"
        "5 3 1 | 4 2 8 | 7 9 6\n"
        "2 8 9 | 6 5 7 | 3 1 4\n"
        "4 6 7 | 3 9 1 | 5 2 8\n"
    )
