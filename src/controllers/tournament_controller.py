from datetime import datetime

from src.models.tournament import Tournament
from src.models.player import Player
from src.views.tournament_view import TournamentView
from src.views.round_view import RoundView
from src.repository.tournament_repository import save_tournaments
from src.utils.id_generator import generate_next_id, IDPrefix


class TournamentController:
    def __init__(self, tournaments: list[Tournament], players: list[Player]):
        self.tournaments = tournaments
        self.players = players
        self.tournament_view = TournamentView()
        self.round_view = RoundView()

    def create_tournament(
            self,
            tournament_data: dict,
    ) -> Tournament:
        """"""
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
                    f"{tournament.start_datetime.strftime("%Y-%m")}\n"
                    f"- city: {tournament.address.city}\n"
                    "already exists."
                )

        existing_ids = [
            tournament.id
            for tournament in self.tournaments
        ]

        tournament.id = generate_next_id(IDPrefix.TOURNAMENT, existing_ids)

        self.tournaments.append(tournament)
        save_tournaments(self.tournaments)
        return tournament

    def get_selectable_players(
            self,
            tournament: Tournament,
    ) -> list[Player]:
        """"""
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
        """"""
        if not isinstance(tournament, Tournament):
            raise TypeError("'tournament' must be a Tournament object.")

        if not isinstance(selectable_players, list):
            raise TypeError("'players' must be a list.")

        for player in selectable_players:
            if not isinstance(player, Player):
                raise TypeError("'players' must contain only Player Object")

        if not isinstance(selected_players_indices, list):
            raise TypeError("'selected_players_indices' must be a list.")

        for index in selected_players_indices:
            if not isinstance(index, int):
                raise TypeError(
                    "'selected_players_indices' must contain "
                    "only integer numbers."
                )

        selected_players = []

        for index in selected_players_indices:
            selected_players.append(selectable_players[index - 1])

        tournament.players.extend(selected_players)
        save_tournaments(self.tournaments)
        return selected_players

    def select_tournament(
            self,
            selected_tournament_index: int,
    ) -> Tournament:
        """"""
        if not isinstance(selected_tournament_index, int):
            raise TypeError(
                "'selected_tournament_index' must be an integer "
            )

        selected_tournament = self.tournaments[selected_tournament_index - 1]

        return selected_tournament

    def start_tournament():
        pass

    def tournament_already_exists(
            self,
            name: str,
            city: str,
            start_datetime: datetime,
    ) -> bool:
        """"""
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
