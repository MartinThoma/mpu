"""Helpers for type annotations."""

# Core Library
import typing
from typing import Any

# Third party
from typing_extensions import Protocol

C = typing.TypeVar("C", bound="Comparable")


class Comparable(Protocol):
    """Type for a function which is comparable to other instances."""

    def __eq__(self, other: Any) -> bool:
        """Check if the comparable is equal to other."""

    def __lt__(self: C, other: C) -> bool:
        """Check if the comparable is less than other."""

    def __gt__(self: C, other: C) -> bool:
        """Check if the comparable is greater than other."""

    def __le__(self: C, other: C) -> bool:
        """Check if the comparable is less than or equal to other."""

    def __ge__(self: C, other: C) -> bool:
        """Check if the comparable is greater than or equal to other."""
