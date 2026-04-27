"""Tournament domain model."""

from datetime import date, datetime

from models.round import Round
from models.player import Player
from utils.validators import (
    validate_non_empty_string,
    validate_regex_match,
    validate_date,
    validate_date_order,
    validate_number,
    validate_class_object,
    STREET_NUMBER_PATTERN,
    STREET_NUMBER_PATTERN_DESCRIPTION,
    POSTAL_CODE_PATTERN,
    POSTAL_CODE_PATTERN_DESCRIPTION
)
from models.lifecycle import EventStatus

DEFAULT_ROUND_NUMBER = 4


class Address:
    """Represent the place address where a tournament takes place."""
    def __init__(
        self,
        street_number: str,
        street_name: str,
        postal_code: str,
        city: str,
    ) -> None:
        self.street_number = validate_regex_match(
            street_number,
            "street_number",
            STREET_NUMBER_PATTERN,
            STREET_NUMBER_PATTERN_DESCRIPTION
        )
        self.street_name = validate_non_empty_string(
            street_name,
            "street_name",
        )
        self.postal_code = validate_regex_match(
            postal_code,
            "postal_code",
            POSTAL_CODE_PATTERN,
            POSTAL_CODE_PATTERN_DESCRIPTION,
        )
        self.city = validate_non_empty_string(city, "city")


class Tournament:
    """Represent a chess tournament, complete or still being prepared.

    A tournament may initially be created with only a name. Optional fields can
    be completed later, but every provided value is validated when assigned.
    Before the tournament can actually be started, required data should be
    checked with validate_ready_to_start().
    """

    def __init__(
            self,
            name: str,
            place: Address | None = None,
            start_date: datetime | None = None,
            end_date: datetime | None = None,
            number_of_players: int | None = None,
            number_of_rounds: int = DEFAULT_ROUND_NUMBER,
            description: str | None = None,
    ):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_players = number_of_players
        self.number_of_rounds = number_of_rounds
        self.description = description
        self.id: int | None = None
        self.list_of_players: list[Player] = []
        self.list_of_rounds: list[Round] = []
        self.current_round: Round | None = None

    @property
    def name(self) -> str:
        """Return the tournament name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = validate_non_empty_string(value, "name")

    @property
    def place(self) -> Address | None:
        """Return the tournament address, if defined."""
        return self._place

    @place.setter
    def place(self, value: Address | None) -> None:
        if value is None:
            self._place = None
            return

        self._place = validate_class_object(value, "place", Address)

    @property
    def start_date(self) -> datetime | None:
        """Return the tournament start date, if defined."""
        return self._start_date

    @start_date.setter
    def start_date(self, value: datetime | None) -> None:
        if value is None:
            self._start_date = None
            return

        validated_date = validate_date(value, "start_date")

        if hasattr(self, "_end_date") and self._end_date is not None:
            validate_date_order(validated_date, self._end_date)

        self._start_date = validated_date

    @property
    def end_date(self) -> datetime | None:
        """Return the tournament end date, if defined."""
        return self._end_date

    @end_date.setter
    def end_date(self, value: datetime | None) -> None:
        if value is None:
            self._end_date = None
            return

        validated_date = validate_date(value, "end_date")

        if hasattr(self, "_start_date") and self._start_date is not None:
            validate_date_order(self._start_date, validated_date)

        self._end_date = validated_date

    @property
    def number_of_players(self) -> int | None:
        """Return the maximum number of players, if defined."""
        return self._number_of_players

    @number_of_players.setter
    def number_of_players(self, value: int | None) -> None:
        self._number_of_players = validate_number(
            value,
            "number_of_players",
            int,
            2
        )

    @property
    def number_of_rounds(self) -> int:
        """Return the number of rounds set for the tournament."""
        return self._number_of_rounds

    @number_of_rounds.setter
    def number_of_rounds(self, value: int):
        self._number_of_rounds = validate_number(
            value,
            "number_of_rounds",
            int,
            1
        )

    @property
    def description(self) -> str | None:
        """Return the tournament description, if defined."""
        return self._description

    @description.setter
    def description(self, value: str | None):
        if value is None:
            self._description = None
            return

        self._description = validate_non_empty_string(value, "description")

    def add_player(self, player: Player) -> None:
        """Add a player to the tournament.

        Raises:
            TypeError: If player is not a Player object.
            ValueError: If the tournament already has the maximum number of
                players.
        """
        validated_player = validate_class_object(player, "player", Player)

        if (
            self.number_of_players is not None
            and len(self.list_of_players) >= self.number_of_players
        ):
            raise ValueError(
                "Maximum number of players set for this tournament "
                "has already been reached."
            )

        self.list_of_players.append(validated_player)

    def create_round(self) -> Round:
        """Create, start, and add the next round to the tournament.

        The round number is automatically computed from the number of rounds
        already registered in the tournament.

        Raises:
            ValueError: If the maximum number of rounds has already been
                reached, or if the previous round is not finished.

        Returns:
            The newly created Round object.
        """
        if len(self.list_of_rounds) >= self.number_of_rounds:
            raise ValueError(
                "Maximum number of rounds set for this tournament "
                "has already been reached."
            )

        if self.list_of_rounds:
            previous_round = self.list_of_rounds[-1]

            if (
                previous_round.end_datetime is None
                or previous_round.status != EventStatus.FINISHED
            ):
                raise ValueError(
                    f"Previous round n° {previous_round.number} "
                    "is still ongoing. Previous round must be finished "
                    "before creating a new round."
                )

        next_round_number = len(self.list_of_rounds) + 1
        new_round = Round(number=next_round_number)
        new_round.start_round()

        self.list_of_rounds.append(new_round)
        self.current_round = new_round

        return new_round

    def validate_ready_to_start(self) -> None:
        """Validate that the tournament has all data required to start.

        Raises:
            ValueError: If required tournament data is missing or inconsistent.
        """
        if self.place is None:
            raise ValueError("Tournament place must be defined before starting.")

        if self.start_date is None:
            raise ValueError(
                "Tournament start date must be defined before starting."
            )

        if self.end_date is None:
            raise ValueError(
                "Tournament end date must be defined before starting."
            )

        if self.number_of_players is None:
            raise ValueError(
                "Tournament number of players must be defined before starting."
            )

        if len(self.list_of_players) < 2:
            raise ValueError("Tournament must have at least two players.")

    def __str__(self):
        """Return the tournament name."""
        return self.name

    def __repr__(self):
        """Return a developer-friendly representation of the tournament."""
        return (
            f"Tournament("
            f"name={self.name!r}, "
            f"players={len(self.list_of_players)!r}, "
            f"rounds={len(self.list_of_rounds)!r}, "
            f"current_round={self.current_round!r}, "
            f"number_of_rounds={self.self.number_of_rounds!r}"
            f")"
        )
