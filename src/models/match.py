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
            ):

        self.white_player = white_player
        self.black_player = black_player
        self.match_id: int | None = None
        self.start_datetime: datetime | None = None
        self.end_datetime: datetime | None = None
        self.status = MatchStatus.IN_COMING
        self.result = None

    @staticmethod
    def _validate_is_a_player(value: str, field_name: str):
        if not isinstance(value, Player):
            raise ValueError(f"'{field_name}' must be a 'Player' object'")

        return value

    @property
    def white_player(self):
        return self._white_player

    @white_player.setter
    def white_player(self, value):
        self._white_player = self._validate_is_a_player(value, "white_player")

    @property
    def black_player(self):
        return self._black_player

    @black_player.setter
    def black_player(self, value):
        self._black_player = self._validate_is_a_player(value, "black_player")

    def start_match(self):
        if (
            self.start_datetime is not None 
            or self.status != MatchStatus.IN_COMING
        ):
            raise ValueError(
                "Match has already started and cannot be started again"
                )

        self.start_datetime = datetime.now()
        self.status = MatchStatus.IN_PROGRESS


    def end_match():
        pass