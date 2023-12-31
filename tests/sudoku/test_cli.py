"""Tests whether the cli runs correctly or not."""

from subprocess import PIPE, run


def test_version_help():
    res = run(["sudoku", "--help"], stdout=PIPE, stderr=PIPE, shell=True)
    assert res.returncode == 0
    assert res.stdout.startswith(b"Usage: sudoku [OPTIONS] FILE_PATH")
