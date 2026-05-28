"""Controller for player creation and persistence."""

from src.models.player import Player
from src.repository.player_repository import save_players


class PlayerController:
    """Coordinate player-related application actions."""

    def __init__(self, players: list[Player]) -> None:
        """Initialize the controller with loaded player objects."""
        self.players = players

    def create_player(self, player_data: dict) -> Player:
        """Create, validate, persist, and return a new player.

        Args:
            player_data: Raw player attributes collected from the view.

        Returns:
            Created player.

        Raises:
            ValueError: If player data is invalid or if another player
                already uses the same chess national ID.
        """
        try:
            player = Player(**player_data)
        except (TypeError, ValueError) as error:
            raise ValueError(f"Invalid player data: {error}") from error

        for existing_player in self.players:
            if existing_player.chess_national_id == player.chess_national_id:
                raise ValueError(
                    f"A player with chess national ID "
                    f"{player.chess_national_id} already exists. "
                    f"The existing player is {existing_player.first_name} "
                    f"{existing_player.last_name}."
                )

        self.players.append(player)
        save_players(self.players)
        return player
