"""Command line interface entrypoint."""

from enum import Enum
from time import time

import typer

from sudoku.sudoku import Sudoku

app = typer.Typer(no_args_is_help=True)


class SudokuDifficulty(Enum):
    """Enumeration of the available difficulties."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


@app.command("solve", no_args_is_help=True)
def solve_sudoku(file_path: str = typer.Argument(..., help="Path to sudoku file.")) -> None:
    """Solves a sudoku."""
    sudoku = Sudoku.from_file(file_path)
    print(sudoku.humanize())

    start = time()
    sudoku.solve()
    sudoku.check_consistency()
    end = time() - start

    print("SOLVED SUDOKU:\n\n" + sudoku.humanize() + "\n")
    print(f"ELAPSED TIME: {end}")
