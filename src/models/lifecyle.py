from enum import Enum

from datetime import datetime

from typing import Protocol


class EventStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"


class EventType(Protocol):
    status: str
    start_datetime: datetime | None
    end_datetime: datetime | None


def start_lifecycle(event: EventType):
    if (
        event.start_datetime is not None
        or event.status != EventStatus.NOT_STARTED
    ):
        raise ValueError(
            f"'{event}' has already started and cannot be started again"
            )

    event.start_datetime = datetime.now()
    event.status = EventStatus.IN_PROGRESS


def end_lifecycle(event: EventType):
    if (
        event.start_datetime is None
        or event.status != EventStatus.IN_PROGRESS
    ):
        raise ValueError(
            f"'{event}' has not started yet and cannot be ended"
        )

    event.end_datetime = datetime.now()
    event.status = EventStatus.FINISHED
