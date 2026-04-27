"""Shared lifecycle helpers for startable and endable domain objects.

This module centralizes the common logic used by objects that follow a
simple lifecycle:

- not started
- in progress
- finished

It is intended for domain entities such as rounds and matches.
"""

from enum import Enum
from datetime import datetime
from typing import Protocol


class EventStatus(Enum):
    """Represent the lifecycle status of a domain event."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"


class EventType(Protocol):
    """Define the attributes required by lifecycle helper functions."""
    status: EventStatus
    start_datetime: datetime | None
    end_datetime: datetime | None


def start_lifecycle(event: EventType) -> None:
    """Start an event if it has not already started.

    Args:
        event: Object with status, start_datetime and end_datetime attributes.

    Raises:
        ValueError: If the event has already started.
    """
    if (
        event.start_datetime is not None
        or event.status != EventStatus.NOT_STARTED
    ):
        raise ValueError(
            f"'{event}' has already started and cannot be started again"
        )

    event.start_datetime = datetime.now()
    event.status = EventStatus.IN_PROGRESS


def end_lifecycle(event: EventType) -> None:
    """End an event if it is currently in progress.

    Args:
        event: Object with status, start_datetime and end_datetime attributes.

    Raises:
        ValueError: If the event has not started or is not in progress.
    """
    if (
        event.start_datetime is None
        or event.status != EventStatus.IN_PROGRESS
    ):
        raise ValueError(
            f"'{event}' has not started yet and cannot be ended"
        )

    event.end_datetime = datetime.now()
    event.status = EventStatus.FINISHED
