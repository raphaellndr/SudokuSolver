import sudoku


def test_version() -> None:
    assert sudoku.__version__ is not None


def test_program_name() -> None:
    assert sudoku.PROGRAM_NAME is not None
