"""Controller for tournament creation and player registration."""

from datetime import datetime

from src.models.player import Player
from src.models.tournament import Tournament
from src.repository.tournament_repository import save_tournaments
from src.utils.id_generator import IDPrefix, generate_next_id


class TournamentController:
    """Coordinate tournament creation, selection, and player assignment."""

    def __init__(
        self,
        tournaments: list[Tournament],
        players: list[Player]
    ) -> None:
        """Initialize the controller with loaded tournaments and players."""
        self.tournaments = tournaments
        self.players = players

    def create_tournament(
        self,
        tournament_data: dict,
    ) -> Tournament:
        """Create, validate, persist, and return a new tournament.

        Args:
            tournament_data: Raw tournament attributes collected from the view.

        Returns:
            Created tournament with generated ID.

        Raises:
            ValueError: If tournament data is invalid or if a duplicate
                tournament already exists.
        """
        try:
            tournament = Tournament(**tournament_data)
        except (TypeError, ValueError) as error:
            raise ValueError(f"Invalid tournament data: {error}") from error

        if self.tournament_already_exists(
            tournament.name,
            tournament.address.city,
            tournament.start_datetime
        ):
            raise ValueError(
                "A tournament with the same:\n"
                f"- name: {tournament.name}\n"
                "- start datetime: "
                f"{tournament.start_datetime.strftime('%Y-%m')}\n"
                f"- city: {tournament.address.city}\n"
                "already exists."
            )

        existing_ids = [
            existing_tournament.id
            for existing_tournament in self.tournaments
        ]

        tournament.id = generate_next_id(IDPrefix.TOURNAMENT, existing_ids)

        self.tournaments.append(tournament)
        save_tournaments(self.tournaments)
        return tournament

    def get_selectable_players(
        self,
        tournament: Tournament,
    ) -> list[Player]:
        """Return players not already registered in the tournament.

        Args:
            tournament: Tournament used to exclude already registered players.

        Returns:
            Players that can still be added to the tournament.
        """
        tournament_players_ids = [
            player.chess_national_id
            for player in tournament.players
        ]

        selectable_players = [
            player
            for player in self.players
            if player.chess_national_id not in tournament_players_ids
        ]

        return selectable_players

    def select_players(
        self,
        tournament: Tournament,
        selectable_players: list[Player],
        selected_players_indices: list[int],
    ) -> list[Player]:
        """Register selected players in a tournament and persist the change.

        Args:
            tournament: Tournament receiving the selected players.
            selectable_players: Players available for selection.
            selected_players_indices: One-based selected indices.

        Returns:
            Players added to the tournament.

        Raises:
            TypeError: If arguments have invalid types.
        """
        if not isinstance(tournament, Tournament):
            raise TypeError("'tournament' must be a Tournament object.")

        self.validate_can_add_players(tournament)

        if not isinstance(selectable_players, list):
            raise TypeError("'players' must be a list.")

        for player in selectable_players:
            if not isinstance(player, Player):
                raise TypeError("'players' must contain only Player objects.")

        if not isinstance(selected_players_indices, list):
            raise TypeError("'selected_players_indices' must be a list.")

        for index in selected_players_indices:
            if not isinstance(index, int):
                raise TypeError(
                    "'selected_players_indices' must contain "
                    "only integer numbers."
                )

        selected_players = [
            selectable_players[index - 1]
            for index in selected_players_indices
        ]

        tournament.players.extend(selected_players)
        save_tournaments(self.tournaments)
        return selected_players

    def select_tournament(
        self,
        selected_tournament_index: int,
    ) -> Tournament:
        """Return the tournament matching a one-based selection index.

        Args:
            selected_tournament_index: User-facing tournament index.

        Returns:
            Selected tournament.

        Raises:
            TypeError: If the selection index is not an integer.
        """
        if not isinstance(selected_tournament_index, int):
            raise TypeError(
                "'selected_tournament_index' must be an integer."
            )

        selected_tournament = self.tournaments[selected_tournament_index - 1]

        return selected_tournament

    def tournament_already_exists(
        self,
        name: str,
        city: str,
        start_datetime: datetime,
    ) -> bool:
        """Check whether a similar tournament already exists.

        A tournament is considered duplicate when it has the same name, city,
        and start month.

        Args:
            name: Tournament name to compare.
            city: Tournament city to compare.
            start_datetime: Tournament start date used for month comparison.

        Returns:
            True if a matching tournament already exists, otherwise False.
        """
        for tournament in self.tournaments:
            if (
                tournament.name.lower() == name.lower()
                and tournament.address.city.lower() == city.lower()
                and (
                    tournament.start_datetime.strftime("%Y-%m")
                    == start_datetime.strftime("%Y-%m")
                )
            ):
                return True

        return False

    def end_tournament(self, selected_tournament: Tournament) -> None:
        """End the selected tournament and persist the updated state."""
        if not isinstance(selected_tournament, Tournament):
            raise TypeError(
                "'selected_tournament' must be a Tournament object."
            )

        selected_tournament.end_tournament()
        save_tournaments(self.tournaments)

    def validate_can_add_players(self, tournament: Tournament) -> None:
        """Ensure players can still be added to the tournament.

        Args:
            tournament: Tournament to validate.

        Raises:
            TypeError: If tournament is not a Tournament instance.
            ValueError: If the tournament has already started.
        """
        if not isinstance(tournament, Tournament):
            raise TypeError("'tournament' must be a Tournament object.")

        if tournament.rounds or tournament.current_round is not None:
            raise ValueError(
                "Cannot add players after the first round has been created."
            )
