"""Module containing methods to solve a sudoku."""

from random import SystemRandom

from .domains import Domain, Domains
from .exceptions import ValueAssignmentError
from .grid import Grid, Index

cryptogen = SystemRandom()

BACKTRACKING_DEPTH_THRESHOLD = cryptogen.randint(35, 65)
BACKTRACKING_PROBABILITY = cryptogen.uniform(0.35, 0.65)


def _assign_value(*, grid: Grid, domains: Domains, value_index: Index) -> None:
    """Assigns a value respecting constraints at the given index and removes it from the domain.

    :param grid: `Grid` containing the Sudoku to solve.
    :param domains: `Domains` containing every cell's domain.
    :param value_index: index of the cell to assign a value to.
    :raises: `ValueAssignmentError` when every value from a domain has been tried unsuccessfully.
    """
    if domains.get_domain(value_index):
        domain = grid.least_constraining_value(value_index)
        for value in domain:
            if grid.check_constraints(value=value, value_index=value_index):
                domain.remove(value)
                grid.domains.set_domain(domain, value_index)
                grid.set_value(value, value_index)
                return
    raise ValueAssignmentError(value_index)


def backtracking(
    *, grid: Grid, domains: Domains, initial_domains: list[list[Domain | None]]
) -> None:
    """Backtracking algorithm for solving Sudoku puzzles.

    :param grid: `Grid` containing the sudoku to solve.
    :param domains: `Domains` containing every cell's domain.
    """
    # AC-3 enforcement
    grid.enforce_arc_consistency()

    assignment_stack: list[Index] = []
    while indexes := grid.minimum_remaining_value():
        index = indexes[0]
        try:
            _assign_value(grid=grid, domains=domains, value_index=index)
            assignment_stack.append(index)
        except ValueAssignmentError:
            domains.reinitialize_domain(domain_index=index, initial_domains=initial_domains)
            # Reset last assignment's value and remove it from the assigment stack
            last_assignment = assignment_stack.pop()
            grid.reinitialize_value(last_assignment)
