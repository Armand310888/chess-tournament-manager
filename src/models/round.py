from datetime import datetime

from models.match import Match
from models.player import Player
from models.lifecyle import start_lifecycle, end_lifecycle, EventStatus
from utils.validators import validate_number


class Round:
    """"""
    def __init__(self) -> None:
        self.list_of_match: list[Match] | None = None
        self.list_of_players: list[Player] | None = None
        self.start_datetime: datetime | None = None
        self.end_datetime: datetime | None = None
        self.number: int | None = None # ici faire quelque chose comme Round 1?
        self.status = EventStatus.NOT_STARTED

    @property
    def number(self):
        """"""
        return self._number

    @number.setter
    def number(self, value):
        self._number = validate_number(
            value,
            "number",
            int,
            1
        )


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