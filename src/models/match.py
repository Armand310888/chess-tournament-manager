"""Match domain model."""

from datetime import datetime
from enum import Enum
import random

from models.player import Player
from models.lifecycle import start_lifecycle, end_lifecycle, EventStatus
from utils.validators import validate_class_object


class MatchResult(Enum):
    """Represent the possible results of a chess match."""
    WHITE_WIN = "white_win"
    BLACK_WIN = "black_win"
    DRAW = "draw"


class Match:
    """Represent a chess match between two players.

    A match stores the two players involved, assigns white and black colors,
    tracks lifecycle dates, and records the final result and scores.
    """
    def __init__(
            self,
            player_1: Player,
            player_2: Player,
    ) -> None:

        self.player_1 = validate_class_object(player_1, "player_1", Player)
        self.player_2 = validate_class_object(player_2, "player_2", Player)

        if self.player_1 is self.player_2:
            raise ValueError("'player_1' must be different from 'player_2'")

        self.match_id: int | None = None
        self.start_datetime: datetime | None = None
        self.end_datetime: datetime | None = None
        self.status = EventStatus.NOT_STARTED
        self.result: MatchResult | None = None
        self.white_player: Player | None = None
        self.black_player: Player | None = None
        self.white_player_score: float | None = None
        self.black_player_score: float | None = None

    def set_black_and_white_player(self) -> None:
        """Randomly assign white and black colors to match players."""
        players = [self.player_1, self.player_2]

        self.white_player = random.choice(players)

        if self.white_player == self.player_1:
            self.black_player = self.player_2
        else:
            self.black_player = self.player_1

    def start_match(self) -> None:
        """Start the match lifecycle."""
        start_lifecycle(self)

    def end_match(self, result: MatchResult):
        """End the match and assign scores according to its result.

        Args:
            result: Final result of the match.

        Raises:
            ValueError: If result is not a MatchResult value.
        """
        if not isinstance(result, MatchResult):
            raise ValueError("'result' must be a MatchResult value")

        end_lifecycle(self)
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

    def __str__(self) -> str:
        """Return a readable match description."""
        return f"{self.white_player} vs {self.black_player}"

    def __repr__(self) -> str:
        """Return a developer-friendly representation of the match."""
        return (
            f"Match("
            f"player_1={self.player_1!r}, "
            f"player_2={self.player_2!r}, "
            f"status={self.status!r}, "
            f"result={self.result!r}"
            f")"
        )
