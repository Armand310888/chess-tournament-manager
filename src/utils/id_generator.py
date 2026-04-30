"""Provide utilities for generating sequential IDs with typed prefixes.

This module defines supported ID prefixes and a helper function to
generate unique, incremented identifiers based on existing IDs.
IDs combine a type-specific prefix and a zero-padded numeric suffix.
"""
from enum import Enum


class IDPrefix(Enum):
    """Enumerate supported ID prefixes."""
    TOURNAMENT = "T"
    ROUND = "R"
    MATCH = "M"


def generate_next_id(prefix: IDPrefix, existing_ids: list[str]) -> str:
    """Generate the next sequential ID for a given prefix.

    Extract numeric parts from existing IDs, compute the next
    available number, and return a zero-padded ID.

    Args:
        prefix: ID prefix enum.
        existing_ids: Existing IDs using the same convention.

    Returns:
        The next generated ID.

    Raises:
        TypeError: If prefix is not an IDPrefix.
    """
    if not isinstance(prefix, IDPrefix):
        raise TypeError("'prefix' must be IDPrefix object.")

    id_numbers = []

    for id in existing_ids:
        if id.startswith(prefix.value):
            id_number = int(id[len(prefix.value):])
            id_numbers.append(id_number)

    next_id_number = max(id_numbers, default=0) + 1

    return f"{prefix.value}{next_id_number:03d}"
