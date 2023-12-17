"""Module containing methods to solve a sudoku."""

import random

from .domains import Domain, Domains
from .exceptions import ValueAssignmentError
from .grid import Grid, Index

BACKTRACKING_DEPTH_THRESHOLD = random.randint(35, 65)
BACKTRACKING_PROBABILITY = random.uniform(0.35, 0.65)


def _assign_value(
    *, grid: Grid, domains: Domains, value_index: Index, depth: int, mode: str
) -> None:
    """Assigns a value respecting constraints at the given index and removes it from the domain.

    If `mode` is set to "generate", enters generation mode: shuffles the domain to introduce
    randomness in value assignment. Furthermore, if the current depth is greater than a certain
    threshold and backtracking probability is met, backtracks to increase the randomness of
    the generation.

    :param grid: `Grid` containing the Sudoku to solve or generate.
    :param domains: `Domains` containing every cell's domain.
    :param value_index: index of the cell to assign a value to.
    :param depth: current depth in the recursion.
    :param mode: string indicating the mode ("solve" or "generate").
    :raises: `ValueAssignmentError` when every value from a domain has been tried unsuccessfully.
    """
    if domains.get_domain(value_index):
        domain = grid.least_constraining_value(value_index)
        if mode == "generate":
            suffled_domain = list(domain)
            random.shuffle(suffled_domain)
            domain = set(suffled_domain)
        for value in domain:
            if grid.check_constraints(value=value, value_index=value_index):
                domain.remove(value)
                grid.domains.set_domain(domain, value_index)
                grid.set_value(value, value_index)
                return
        if (
            mode == "generate"
            and depth > BACKTRACKING_DEPTH_THRESHOLD
            and random.random() < BACKTRACKING_PROBABILITY
        ):
            raise ValueAssignmentError(value_index)
    raise ValueAssignmentError(value_index)


def backtracking(
    *, grid: Grid, domains: Domains, initial_domains: list[list[Domain | None]], mode: str = "solve"
) -> None:
    """Backtracking algorithm for solving or generating Sudoku puzzles.

    :param grid: `Grid` containing the sudoku to solve or generate.
    :param domains: `Domains` containing every cell's domain.
    :param mode: string indicating the mode ("solve" or "generate").
    """
    # AC-3 enforcement
    grid.enforce_arc_consistency()

    assignment_stack: list[Index] = []
    depth = 0
    while indexes := grid.minimum_remaining_value():
        index = indexes[0]
        try:
            _assign_value(grid=grid, domains=domains, value_index=index, depth=depth, mode=mode)
            assignment_stack.append(index)
            depth += 1
        except ValueAssignmentError:
            domains.reinitialize_domain(domain_index=index, initial_domains=initial_domains)
            # Reset last assignment's value and remove it from the assigment stack
            last_assignment = assignment_stack.pop()
            grid.reinitialize_value(last_assignment)
            depth -= 1
