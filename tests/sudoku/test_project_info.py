import sudoku_resolver


def test_version() -> None:
    assert sudoku_resolver.__version__ is not None


def test_program_name() -> None:
    assert sudoku_resolver.PROGRAM_NAME is not None
