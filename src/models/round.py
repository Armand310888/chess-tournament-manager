"""Round domain model."""

from datetime import datetime

from models.match import Match
from models.lifecycle import start_lifecycle, end_lifecycle, EventStatus
from utils.validators import validate_number
from repository.match_repository import get_match_by_id


class Round:
    """Represent a tournament round containing several matches.

    A round has a number, a list of matches, lifecycle dates, and a status.
    It can be started and ended through the shared lifecycle helpers."""

    def __init__(self, number: int) -> None:
        self.number = number
        self.matches: list[Match] = []
        self.start_datetime: datetime | None = None
        self.end_datetime: datetime | None = None
        self.status = EventStatus.NOT_STARTED
        self.id: str | None = None

    @property
    def number(self) -> int:
        """"""
        return self._number

    @number.setter
    def number(self, value: int) -> None:
        self._number = validate_number(
            value,
            "number",
            int,
            1,
        )

    def add_match(self, match: Match) -> None:
        """Add a match to the round.

        Args:
            match: Match object to add to the round.

        Raises:
            TypeError: If match is not a Match object.
        """
        if not isinstance(match, Match):
            raise TypeError("'match' must be a Match object.")

        self.matches.append(match)

    def start_round(self) -> None:
        """Start the round lifecycle."""
        start_lifecycle(self)

    def end_round(self) -> None:
        """End the round lifecycle."""
        end_lifecycle(self)

    def to_dict(self) -> dict:
        """Return a JSON-serializable dictionary representation of the round.

        Match objects are represented by their IDs. Datetime fields are
        converted to ISO-formatted strings.
        """
        matches_id = [match.id for match in self.matches]

        return {
            "number": self.number,
            "matches_id": matches_id,
            "start_datetime": (
                self.start_datetime.isoformat()
                if self.start_datetime else None
            ),
            "end_datetime": (
                self.end_datetime.isoformat()
                if self.end_datetime else None
            ),
            "status": self.status.value,
            "id": self.id,
        }

    @classmethod
    def from_dict(cls, data: dict, matches: list[Match]) -> "Round":
        """Rebuild a Round from serialized data.

        Resolve match IDs to Match objects and restore datetime and
        enum fields to their Python representations.

        Args:
            data: Serialized round data.
            matches: Available matches used for ID resolution.

        Returns:
            A reconstructed Round instance.

        Raises:
            TypeError: If data is not a dictionary.
            ValueError: If a field is missing, invalid, or references
                an unknown match.
        """
        if not isinstance(data, dict):
            raise TypeError("'data' must be a dictionary.")

        try:
            round = Round(data["number"])

            matches_id = data["matches_id"]
            round.matches = [
                get_match_by_id(match_id, matches)
                for match_id in matches_id
            ]

            round.start_datetime = (
                datetime.fromisoformat(data["start_datetime"])
                if data.get("start_datetime") else None
            )

            round.end_datetime = (
                datetime.fromisoformat(data["end_datetime"])
                if data.get("end_datetime") else None
            )

            round.status = EventStatus(data["status"])

            round.id = data["id"]

            return round

        except KeyError as missing_field:
            raise ValueError(
                f"Missing field: {missing_field.args[0]}"
            ) from missing_field

    def __str__(self) -> str:
        """Return a readable round description."""
        return f"Round {self.number}"

    def __repr__(self) -> str:
        """Return a developer-friendly representation of the round."""
        return (
            f"Round("
            f"number={self.number!r}, "
            f"matches={len(self.matches)!r}, "
            f"status={self.status!r}"
            f")"
        )
