"""Tournament domain model."""

from datetime import datetime

from models.round import Round
from models.player import Player
from utils.validators import (
    validate_non_empty_string,
    validate_regex_match,
    validate_date,
    validate_date_order,
    validate_number,
    validate_class_object,
    Pattern,
    PatternDescription,
)
from models.lifecycle import EventStatus
from repository.player_repository import get_player_by_id
from repository.round_repository import get_round_by_id

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
            Pattern.STREET_NUMBER,
            PatternDescription.STREET_NUMBER
        )
        self.street_name = validate_non_empty_string(
            street_name,
            "street_name",
        )
        self.postal_code = validate_regex_match(
            postal_code,
            "postal_code",
            Pattern.POSTAL_CODE,
            PatternDescription.POSTAL_CODE,
        )
        self.city = validate_non_empty_string(city, "city")

    def to_dict(self):
        """Return a JSON-serializable representation of the address.

        Converts the Address instance into a dictionary suitable for
        JSON storage.

        Returns:
            A dictionary containing the address fields.
        """
        return {
            "street_number": self.street_number,
            "street_name": self.street_name,
            "postal_code": self.postal_code,
            "city": self.city
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create an Address instance from a dictionary.

        Reconstructs an Address object from serialized data.

        Args:
            data: Dictionary containing address fields.

        Returns:
            An Address instance.

        Raises:
            TypeError: If 'data' is not a dictionary.
            ValueError: If required fields are missing.
        """
        address = cls(
            street_number=data["street_number"],
            street_name=data["street_name"],
            postal_code=data["postal_code"],
            city=data["city"],
        )

        return address


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
            address: Address | None = None,
            start_datetime: datetime | None = None,
            end_datetime: datetime | None = None,
            number_of_players: int | None = None,
            number_of_rounds: int = DEFAULT_ROUND_NUMBER,
            description: str | None = None,
    ):
        self.name = name
        self.address = address
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.number_of_players = number_of_players
        self.number_of_rounds = number_of_rounds
        self.description = description
        self.id: int | None = None
        self.players: list[Player] = []
        self.rounds: list[Round] = []
        self.current_round: Round | None = None

    @property
    def name(self) -> str:
        """Return the tournament name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = validate_non_empty_string(value, "name")

    @property
    def address(self) -> Address | None:
        """Return the tournament address, if defined."""
        return self._address

    @address.setter
    def address(self, value: Address | None) -> None:
        if value is None:
            self._address = None
            return

        self._address = validate_class_object(value, "place", Address)

    @property
    def start_datetime(self) -> datetime | None:
        """Return the tournament start date, if defined."""
        return self._start_datetime

    @start_datetime.setter
    def start_datetime(self, value: datetime | None) -> None:
        if value is None:
            self._start_datetime = None
            return

        validated_date = validate_date(value, "start_datetime")

        if hasattr(self, "_end_datetime") and self._end_datetime is not None:
            validate_date_order(validated_date, self._end_datetime)

        self._start_datetime = validated_date

    @property
    def end_datetime(self) -> datetime | None:
        """Return the tournament end date, if defined."""
        return self._end_datetime

    @end_datetime.setter
    def end_datetime(self, value: datetime | None) -> None:
        if value is None:
            self._end_datetime = None
            return

        validated_date = validate_date(value, "end_date")

        if hasattr(self, "_start_date") and self._start_datetime is not None:
            validate_date_order(self._start_datetime, validated_date)

        self._end_datetime = validated_date

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
            and len(self.players) >= self.number_of_players
        ):
            raise ValueError(
                "Maximum number of players set for this tournament "
                "has already been reached."
            )

        self.players.append(validated_player)

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
        if len(self.rounds) >= self.number_of_rounds:
            raise ValueError(
                "Maximum number of rounds set for this tournament "
                "has already been reached."
            )

        if self.rounds:
            previous_round = self.rounds[-1]

            if (
                previous_round.end_datetime is None
                or previous_round.status != EventStatus.FINISHED
            ):
                raise ValueError(
                    f"Previous round n° {previous_round.number} "
                    "is still ongoing. Previous round must be finished "
                    "before creating a new round."
                )

        next_round_number = len(self.rounds) + 1
        new_round = Round(number=next_round_number)
        new_round.start_round()

        self.rounds.append(new_round)
        self.current_round = new_round

        return new_round

    def validate_ready_to_start(self) -> None:
        """Validate that the tournament has all data required to start.

        Raises:
            ValueError: If required tournament data is missing or inconsistent.
        """
        if self.place is None:
            raise ValueError(
                "Tournament place must be defined before starting."
            )

        if self.start_datetime is None:
            raise ValueError(
                "Tournament start date must be defined before starting."
            )

        if self.end_datetime is None:
            raise ValueError(
                "Tournament end date must be defined before starting."
            )

        if self.number_of_players is None:
            raise ValueError(
                "Tournament number of players must be defined before starting."
            )

        if len(self.players) < 2:
            raise ValueError("Tournament must have at least two players.")

    def to_dict(self) -> dict:
        """Convert the tournament into a JSON-serializable dictionary.

        This method prepares the tournament data for storage by:
        - converting nested objects (Address) into dictionaries
        - converting datetime fields into ISO-formatted strings
        - replacing related objects (players, rounds) with their IDs

        Returns:
            A dictionary representing the tournament,
            ready to be serialized to JSON.
        """
        players_id = [player.chess_national_id for player in self.players]

        rounds_id = [round.id for round in self.rounds]

        return {
            "name": self.name,
            "address": (
                self.address.to_dict()
                if self.address else None
            ),
            "start_datetime": (
                self.start_datetime.isoformat()
                if self.start_datetime else None
            ),
            "end_datetime": (
                self.end_datetime.isoformat()
                if self.end_datetime else None
            ),
            "number_of_players": (
                self.number_of_players
                if self.number_of_players else None
            ),
            "number_of_rounds": self.number_of_rounds,
            "description": (
                self.description
                if self.description else None
            ),
            "id": self.id,
            "players_id": players_id,
            "rounds_id": rounds_id,
            "current_round_id": (
                self.current_round.id
                if self.current_round.id else None
            ),
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
        players: list[Player],
        rounds: list[Round]
    ) -> "Tournament":
        """Create a Tournament instance from a dictionary.

        Reconstructs a Tournament from serialized data. Address is rebuilt
        from nested data, while players and rounds are resolved from their
        stored IDs.

        Args:
            data: Dictionary containing serialized tournament data.

        Returns:
            A Tournament instance.

        Raises:
            TypeError: If 'data' is not a dictionary.
            ValueError: If a required field is missing or invalid.
        """
        if not isinstance(data, dict):
            raise TypeError("'data' must be a dictionary.")

        try:
            address = (
                Address.from_dict(data["address"])
                if data.get("address") is not None
                else None
            )

            players_id = data.get("players_id") or []
            players = [get_player_by_id(player_id) for player_id in players_id]

            rounds_id = data.get("rounds_id") or []
            rounds = [get_round_by_id(round_id) for round_id in rounds_id]

            tournament = cls(
                name=data["name"],
                address=address,
                start_datetime=(
                    datetime.fromisoformat(data["start_datetime"])
                    if data.get("start_datetime") else None
                ),
                end_datetime=(
                    datetime.fromisoformat(data["end_datetime"])
                    if data.get("end_datetime") else None
                ),
                number_of_players=data.get("number_of_players"),
                number_of_rounds=data.get("number_of_rounds"),
                description=data.get("description"),
            )

            tournament.id = data["id"]
            tournament.players = players
            tournament.rounds = rounds
            tournament.current_round = (
                get_round_by_id(data["current_round_id"])
                if data.get("current_round_id") else None
            )

            return tournament

        except KeyError as missing_field:
            raise ValueError(
                f"Missing field: {missing_field.args[0]}"
            ) from missing_field

    def __str__(self):
        """Return the tournament name."""
        return self.name

    def __repr__(self):
        """Return a developer-friendly representation of the tournament."""
        return (
            f"Tournament("
            f"name={self.name!r}, "
            f"players={len(self.players)!r}, "
            f"rounds={len(self.rounds)!r}, "
            f"current_round={self.current_round!r}, "
            f"number_of_rounds={self.number_of_rounds!r}"
            f")"
        )
