"""Module defining a sudoku grid."""

import copy
from collections import deque
from functools import cache, reduce
from typing import Deque, TypeAlias

import numpy as np
from numpy import typing as npt

from .domains import Domains
from .exceptions import ValueAssignmentError

Index: TypeAlias = tuple[int, int]


class Grid:
    """Sudoku grid containing all values."""

    def __init__(self, values: npt.NDArray[np.uint8]) -> None:
        self._values = values

        self.domains = Domains()
        self.preprocess_domains(self.domains)
        self.initial_domains = copy.deepcopy(self.domains.domains)

        self._initial_assigned_values_indexes = self.assigned_values_indexes

    @property
    def unassigned_values_indexes(self) -> list[Index]:
        """Returns unassigned values indexes."""
        return list(tuple(index) for index in np.argwhere(self._values == 0))  # type: ignore

    @property
    def assigned_values_indexes(self) -> list[Index]:
        """Returns assigned values indexes."""
        return list(tuple(index) for index in np.argwhere(self._values != 0))  # type: ignore

    def get_value(self, value_index: Index, /) -> int:
        """Gets the value at given index.

        :param value_index: index of the value to get.
        :returns: value at given index.
        """
        return self._values[value_index[0]][value_index[1]]

    def set_value(self, value: int, value_index: Index) -> None:
        """Sets the value at given index.

        :param value: value to set.
        :param value_index: index of the value to set.
        :raises `ValueAssignmentError`
        """
        if value_index in self._initial_assigned_values_indexes:
            raise ValueAssignmentError(value_index)
        self._values[value_index[0]][value_index[1]] = value

    def reinitialize_value(self, value_index: Index, /) -> None:
        """Reinitializes a value (sets it to 0).

        :param value_index: index of the value to reinitialize.
        """
        self.set_value(0, value_index)

    def preprocess_domains(self, domains: Domains) -> None:
        """Removes inconsistent values from domains.

        :param domains: domains to clean.
        """
        for index in self.assigned_values_indexes:
            domains.set_domain(None, index)
        for index in self.unassigned_values_indexes:
            neighbor_values = set()
            for neighbor_index in self.get_neighbours_indexes(index):
                if domains.get_domain(neighbor_index) is None:
                    neighbor_values.add(self.get_value(neighbor_index))
            domains.domains[index[0]][index[1]] -= neighbor_values  # type:ignore

    def get_horizontal_neighbours_indexes(self, value_index: Index, /) -> list[Index]:
        """Gets horizontal neighbours indexes.

        :param value_index: index of the value to get neighbours indexes from.
        :returns: list containing neighbours' indexes in the row.
        """
        i = value_index[0]
        return [(i, j) for j in range(9) if (i, j) != value_index]

    def get_vertical_neighbours_indexes(self, value_index: Index, /) -> list[Index]:
        """Gets vertical neighbours indexes.

        :param value_index: index of the value to get neighbours indexes from.
        :returns: list containing neighbours' indexes in the column.
        """
        j = value_index[1]
        return [(i, j) for i in range(9) if (i, j) != value_index]

    def get_subgrid_neighbours_indexes(self, value_index: Index, /) -> list[Index]:
        """Gets subgrid neighbours indexes.

        :param value_index: index of the value to get the subgrid neighbours indexes from.
        :returns: list containing neighbours' indexes in the subgrid.
        """
        i, j = value_index
        return list(
            (i_, j_)
            for i_ in range(i // 3 * 3, i // 3 * 3 + 3)
            for j_ in range(j // 3 * 3, j // 3 * 3 + 3)
            if (i_, j_) != (i, j)
        )

    @cache  # pylint: disable=method-cache-max-size-none
    def get_neighbours_indexes(self, value_index: Index, /) -> list[Index]:
        """Gets all neighbours indexes.

        :param value_index: index of the value to get the neighbours indexes from.
        :returns: list containing every indexes.
        """
        return list(
            set(
                self.get_horizontal_neighbours_indexes(value_index)
                + self.get_vertical_neighbours_indexes(value_index)
                + self.get_subgrid_neighbours_indexes(value_index)
            )
        )

    def get_neighbours_values(self, value_index: Index, /) -> list[int]:
        """Gets all neighbours values.

        :param value_index: index of the value to get the neighbours values from.
        :returns: list containing every values.
        """
        return [self.get_value(index) for index in self.get_neighbours_indexes(value_index)]

    def get_neighbours_domains_values(self, value_index: Index, /) -> list[int]:
        """Gets all neighbours' domains values.

        :param value_index: index of the value to get the neighbours domains values from.
        :returns: list containing every values.
        """
        return reduce(
            lambda x, y: x + y,
            [
                list(self.domains.get_domain(index) or [])
                for index in self.get_neighbours_indexes(value_index)
            ],
        )

    def check_constraints(self, *, value: int, value_index: Index) -> bool:
        """Checks if every constraint is respected for a given value.

        :param value: value to check in the grid.
        :param value_index: index of the value to check.
        :returns: `True` if every contraint is respected, `False` otherwise.
        """
        return value not in self.get_neighbours_values(value_index)

    def minimum_remaining_value(self) -> list[Index]:
        """Gets the position of the value with the smallest domain.

        If several values have the same domain length, returns a list of their positions.

        :returns: position(s) of value(s) with smallest domain.
        """
        max_domain_size = 10
        smallest_set_indexes: list[Index] = []

        for value_index in self.unassigned_values_indexes:
            domain = self.domains.get_domain(value_index)
            if domain is not None:
                domain_size = len(domain)
                if domain_size < max_domain_size:
                    max_domain_size = domain_size
                    smallest_set_indexes = [value_index]
                elif domain_size == max_domain_size:
                    smallest_set_indexes.append(value_index)
        return smallest_set_indexes

    def least_constraining_value(self, value_index: Index) -> set[int]:
        """Returns a list of the values to test, ordered by number of occurences in neighbours'
        domains.

        :param value_index: index of the value's domain to order.
        returns: ordered domain values.
        """
        neighbours_domains_values = self.get_neighbours_domains_values(value_index)
        count: dict[int, int] = {}
        for value in self.domains.get_domain(value_index):  # type: ignore
            count[value] = neighbours_domains_values.count(value)
        sorted_count = sorted(count.items(), key=lambda x: x[1])
        return set(list(zip(*sorted_count))[0])

    def enforce_arc_consistency(self) -> None:
        """Enforces arc-consistency algorithm (AC-3) on the sudoku."""
        queue: Deque = deque()

        for value_index in self.unassigned_values_indexes:
            for neighbour in self.get_neighbours_indexes(value_index):
                queue.append((value_index, neighbour))

        while queue:
            value_index, neighbour_index = queue.popleft()
            if self._revise(value_index, neighbour_index):
                if not self.domains.get_domain(value_index):
                    return
                for neighbour in self.get_neighbours_indexes(value_index):
                    queue.append((neighbour, value_index))

    def _revise(self, value_index: Index, neighbour_index: Index) -> bool:
        """Removes inconsistent values from the domain of the cell.

        :param value_index: cell to check for consistency.
        :param neighbour_index: neighbour to check the consistency with.
        :returns: boolean whether a valiue has been removed or not.
        """
        domain = self.domains.get_domain(value_index)
        neighbour_domain = self.domains.get_domain(neighbour_index)
        revised = False
        if domain and neighbour_domain:
            for value in domain.copy():
                if not any(value != neighbour_value for neighbour_value in neighbour_domain):
                    self.domains.pop_value_from_domain(value, value_index)
                    revised = True
        return revised
