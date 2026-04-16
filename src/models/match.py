from datetime import datetime
from enum import Enum

from models.player import Player


class MatchStatus(Enum):
    IN_COMING = "in_coming"
    IN_PROGRESS = "in_progress"
    OVER = "over"


class Match:
    def __init__(
            self,
            white_player: Player,
            black_player: Player,
            match_id: int,
            ):

        self.white_player = white_player
        self.black_player = black_player
        self.match_id = match_id
        self.start_datetime: datetime | None = None
        self.end_datetime: datetime | None = None
        self.status = MatchStatus.IN_COMING
        self.result = None

    @property
    def white_player(self):
        return self._white_player

    @white_player.setter
    def white_player(self, value):
        if not isinstance(value, Player):
            raise ValueError("'white_player' must be a Player object")

        self._white_player = value

    def start_match():
        pass

    def end_match():
        pass