"""Module defining custom exceptions."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .grid import Index


class ConsistencyError(Exception):
    """Sudoku consistency error.

    Raised when a sudoku doesn't respect all constraints.
    """

    def __init__(self, *, value_index: "Index") -> None:
        self.value_index = value_index

    def __str__(self) -> str:
        return (
            f"Sudoku isn't consistent. Value at index '{self.value_index}' "
            "does't respect every constraint"
        )


class ValueAssignmentError(Exception):
    """Value assignment error.

    Raised when the assignment of a value fails.
    """

    def __init__(self, value_index: "Index") -> None:
        self.value_index = value_index

    def __str__(self) -> str:
        return f"Failed to assign a value at given index '{self.value_index}'"
