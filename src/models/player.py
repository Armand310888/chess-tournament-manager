"""Player domain model."""

from utils.validators import (
    validate_non_empty_string,
    validate_date,
    validate_regex_match,
    validate_number,
    CHESS_NATIONAL_ID_PATTERN,
    CHESS_NATIONAL_ID_PATTERN_DESCRIPTION,
    ELO_MAXIMUM,
    ELO_MINIMUM
)

from datetime import date


class Player:
    """Represent a chess player registerd in the application."""
    def __init__(
        self,
        first_name: str,
        last_name: str,
        birth_date: date,
        elo_rating: int,
        chess_national_id: str,
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.elo_rating = elo_rating
        self.chess_national_id = chess_national_id

    @property
    def first_name(self) -> str:
        """Return the player's first name."""
        return self._first_name

    @first_name.setter
    def first_name(self, value: str) -> None:
        self._first_name = validate_non_empty_string(value, "first_name")

    @property
    def last_name(self) -> str:
        """Return the player's last name."""
        return self._last_name

    @last_name.setter
    def last_name(self, value: str) -> None:
        self._last_name = validate_non_empty_string(value, "last_name")

    @property
    def birth_date(self) -> date:
        """Return the player's birth date."""
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value: date) -> None:
        self._birth_date = validate_date(value, "birth_date")

    @property
    def elo_rating(self) -> int:
        """Return the player's ELO rating."""
        return self._elo_rating

    @elo_rating.setter
    def elo_rating(self, value: int) -> None:
        self._elo_rating = validate_number(
            value,
            "elo_rating",
            int,
            ELO_MINIMUM,
            ELO_MAXIMUM,
        )

    @property
    def chess_national_id(self) -> str:
        """Return the player's national chess identifier."""
        return self._chess_national_id

    @chess_national_id.setter
    def chess_national_id(self, value: str) -> None:
        self._chess_national_id = validate_regex_match(
            value,
            "chess_national_id",
            CHESS_NATIONAL_ID_PATTERN,
            CHESS_NATIONAL_ID_PATTERN_DESCRIPTION
            )

    def __str__(self) -> str:
        """Return the player's display name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        """Return a developer-friendly representation of the player."""
        return (
            f"Player("
            f"first_name={self.first_name!r}, "
            f"last_name={self.last_name!r}, "
            f"birth_date={self.birth_date!r}, "
            f"elo_rating={self.elo_rating!r}, "
            f"chess_national_id={self.chess_national_id!r}"
            f")"
        )
