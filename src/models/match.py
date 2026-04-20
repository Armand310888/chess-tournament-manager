from datetime import datetime
from enum import Enum
from models.player import Player

from models.lifecyle import start_lifecycle, end_lifecycle, EventStatus


class MatchResult(Enum):
    WHITE_WIN = "white_win"
    BLACK_WIN = "black_win"
    DRAW = "draw"


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
        self.status = EventStatus.NOT_STARTED
        self.result: MatchResult | None = None
        self.white_player_score: float | None = None
        self.black_player_score: float | None = None

    @staticmethod
    def _validate_is_a_player(value: Player, field_name: str):
        if not isinstance(value, Player):
            raise ValueError(f"'{field_name}' must be a 'Player' object")

        return value

    @property
    def white_player(self):
        return self._white_player

    @white_player.setter
    def white_player(self, value):
        if value is self.black_player:
            raise ValueError("White player must be different to Black player")

        self._white_player = self._validate_is_a_player(value, "white_player")

    @property
    def black_player(self):
        return self._black_player

    @black_player.setter
    def black_player(self, value):
        self._black_player = self._validate_is_a_player(value, "black_player")

    def start_match(self):
        start_lifecycle(self)

    def end_match(self, result: MatchResult):
        end_lifecycle(self)

        if not isinstance(result, MatchResult):
            raise ValueError("result must be a MatchResult value")

        self.result = result

        if result == MatchResult.WHITE_WIN:
            self.white_player_score = 1
            self.black_player_score = 0

        elif result == MatchResult.BLACK_WIN:
            self.black_player_score = 1
            self.white_player_score = 0

        elif result == MatchResult.DRAW:
            self.white_player_score = 0.5
            self.black_player_score = 0.5
