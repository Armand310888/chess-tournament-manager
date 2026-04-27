"""Round domain model."""

from datetime import datetime

from models.match import Match
from models.lifecycle import start_lifecycle, end_lifecycle, EventStatus
from utils.validators import validate_number


class Round:
    """Represent a tournament round containing several matches.

    A round has a number, a list of matches, lifecycle dates, and a status.
    It can be started and ended through the shared lifecycle helpers."""

    def __init__(self, number: int) -> None:
        self.number = number
        self.list_of_matches: list[Match] = []
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

        self.list_of_matches.append(match)

    def start_round(self) -> None:
        """Start the round lifecycle."""
        start_lifecycle(self)

    def end_round(self) -> None:
        """End the round lifecycle."""
        end_lifecycle(self)

    def __str__(self) -> str:
        """Return a readable round description."""
        return f"Round {self.number}"

    def __repr__(self) -> str:
        """Return a developer-friendly representation of the round."""
        return (
            f"Round("
            f"number={self.number!r}, "
            f"matches={len(self.list_of_matches)!r}, "
            f"status={self.status!r}"
            f")"
        )
