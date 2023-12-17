"""Domains tests module."""

import pytest
from sudoku.domains import Domain
from sudoku.grid import Index
from sudoku.sudoku import Sudoku

from tests import SUDOKU_PATH


@pytest.mark.parametrize(
    "domain_index,expected_domain", [((0, 1), {7, 8, 9}), ((2, 7), {2, 5, 8, 9})]
)
def test_reinitialize_domain(domain_index: Index, expected_domain: Domain | None) -> None:
    sudoku = Sudoku(SUDOKU_PATH)
    sudoku.grid.domains.set_domain({99}, domain_index)
    sudoku.grid.domains.reinitialize_domain(
        domain_index=domain_index, initial_domains=sudoku.grid.initial_domains
    )

    assert sudoku.grid.domains.get_domain(domain_index) == expected_domain


@pytest.mark.parametrize(
    "domain_index,expected_domain",
    [
        ((0, 0), None),
        ((3, 7), {1, 5, 6, 9}),
    ],
)
def test_get_domain(domain_index: Index, expected_domain: Domain | None) -> None:
    sudoku = Sudoku(SUDOKU_PATH)
    domain = sudoku.grid.domains.get_domain(domain_index)

    assert domain == expected_domain


@pytest.mark.parametrize(
    "domain_index,expected_domain",
    [
        ((0, 1), {1}),
        ((3, 7), {1, 2, 3, 9}),
    ],
)
def test_set_domain(domain_index: Index, expected_domain: Domain | None) -> None:
    sudoku = Sudoku(SUDOKU_PATH)
    sudoku.grid.domains.set_domain(expected_domain, domain_index)

    assert sudoku.grid.domains.get_domain(domain_index) == expected_domain


def test_set_none_domain() -> None:
    sudoku = Sudoku(SUDOKU_PATH)

    with pytest.raises(ValueError):
        sudoku.grid.domains.set_domain(set(), (0, 0))


@pytest.mark.parametrize(
    "domain_index,value,expected_domain",
    [
        ((0, 1), 8, {7, 9}),
        ((3, 7), 5, {1, 6, 9}),
    ],
)
def test_pop_value_from_domain(
    domain_index: Index, value: int, expected_domain: Domain | None
) -> None:
    sudoku = Sudoku(SUDOKU_PATH)
    sudoku.grid.domains.pop_value_from_domain(value, domain_index)
    domain = sudoku.grid.domains.get_domain(domain_index)

    assert domain == expected_domain
