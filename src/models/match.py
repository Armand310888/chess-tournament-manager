"""Match domain model."""

from datetime import datetime
from enum import Enum
import random

from models.player import Player
from models.lifecycle import start_lifecycle, end_lifecycle, EventStatus
from utils.validators import validate_class_object
from controllers.player_controller import get_player_by_id


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

        self.id: int | None = None
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

    def to_dict(self) -> dict:
        """Convert the match instance into a JSON-serializable dictionary.

        This method prepares match data for storage by converting
        non-serializable fields (such as datetime and enum values)
        into compatible formats and by replacing player objects
        with their unique identifiers.

        Returns:
            A dictionary with the match data, ready to be written to JSON.
        """
        return {
            "player_1_id": self.player_1.chess_national_id,
            "player_2_id": self.player_2.chess_national_id,
            "id": self.id,
            "start_datetime": (
                self.start_datetime.isoformat()
                if self.start_datetime else None
            ),
            "end_datetime": (
                self.end_datetime.isoformat()
                if self.end_datetime else None
            ),
            "status": self.status.value,
            "result": (
                self.result.value
                if self.result else None
            ),
            "white_player_id": (
                self.white_player.chess_national_id
                if self.white_player else None
            ),
            "black_player_id": (
                self.black_player.chess_national_id
                if self.black_player else None
            ),
            "white_player_score": self.white_player_score,
            "black_player_score": self.black_player_score
        }

    @classmethod
    def from_dict(cls, data: dict, players: list[Player]) -> "Match":
        """Create a Match instance from a serialized dictionary.

        This method reconstructs a match object from data previously stored
        in JSON format. It converts serialized datetime and enum values back
        into their Python types and resolves player identifiers into Player
        objects.

        Args:
            data: Dictionary containing the serialized match data.
            players: List of available players used to resolve player IDs.

        Returns:
            A Match instance built from the provided data.

        Raises:
            TypeError: If data is not a dictionary.
            ValueError: If a required field is missing, invalid, or references
                an unknown player.
        """
        if not isinstance(data, dict):
            raise TypeError("'data' must be a dictionary.")

        try:
            player_1 = get_player_by_id(data["player_1_id"], players)
            player_2 = get_player_by_id(data["player_2_id"], players)

            match = cls(player_1, player_2)

            match.id = data["id"]

            match.start_datetime = (
                datetime.fromisoformat(data["start_datetime"])
                if data.get("start_datetime") else None
            )
            match.end_datetime = (
                datetime.fromisoformat(data["end_datetime"])
                if data.get("end_datetime") else None
            )

            match.status = EventStatus(data["status"]),

            match.result = (
                MatchResult(data["result"])
                if data.get("result") else None
            )

            match.white_player = (
                get_player_by_id(data["white_player_id"], players)
                if data.get("white_player_id") else None
            )
            match.black_player = (
                get_player_by_id(data["black_player_id"], players)
                if data.get("black_player_id") else None
            )

            match.white_player_score = data.get("white_player_score")
            match.black_player_score = data.get("black_player_score")

            return match

        except KeyError as missing_field:
            raise ValueError(f"Missing field: {missing_field}")

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
