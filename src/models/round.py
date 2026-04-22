from datetime import datetime

from models.match import Match
from models.lifecyle import start_lifecycle, end_lifecycle, EventStatus


class Round:
    def __init__(
            self,
            list_of_match: list[Match]
            ):

        self.list_of_match = list_of_match
        self.start_datetime: datetime | None = None
        self.end_datetime: datetime | None = None
        self.round_name: str | None = None
        self.status = EventStatus.NOT_STARTED

    def start_round(self) -> None:
        """"""
        start_lifecycle(self)

    def end_round(self) -> None:
        """"""
        end_lifecycle(self)

    def __str__(self):
        pass

    def __repr__(self):
        pass