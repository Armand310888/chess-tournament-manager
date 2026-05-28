"""Shared lifecycle helpers for startable and endable domain objects.

This module centralizes the common logic used by objects that follow a
simple lifecycle:

- in progress
- finished

It is intended for domain entities such as rounds and matches.
"""

from datetime import datetime
from enum import Enum
from typing import Protocol


class EventStatus(Enum):
    """Represent the supported lifecycle states of a domain event."""

    IN_PROGRESS = "in_progress"
    FINISHED = "finished"


class EventType(Protocol):
    """Specify the attributes required by lifecycle helpers."""

    status: EventStatus
    start_datetime: datetime | None
    end_datetime: datetime | None


def end_event(event: EventType) -> None:
    """Mark an in-progress event as finished.

    The helper sets the event end date to the current datetime and updates
    its status to finished.

    Args:
        event: Object exposing lifecycle status and date attributes.

    Raises:
        ValueError: If the event has not started or has already ended.
    """
    if event.start_datetime is None:
        raise ValueError(
            f"'{event}' has not started yet and cannot be ended."
        )

    if event.status == EventStatus.FINISHED:
        raise ValueError(f"'{event}' has already ended.")

    event.end_datetime = datetime.now()
    event.status = EventStatus.FINISHED
