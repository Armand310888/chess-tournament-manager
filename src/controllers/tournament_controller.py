from datetime import datetime
import random

from src.models.tournament import Tournament
from src.models.round import Round
from src.models.player import Player
from src.models.match import Match
from src.models.lifecycle import EventStatus
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
                    f"{tournament.start_datetime.sfrtime("%Y-%m")}\n"
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

        if not selectable_players:
            print("No players selectable for this tournament.")

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

    def create_new_round(self, tournament: Tournament):
        choice = self.round_view.prompt_for_new_round()

        if choice != "y":
            return None

        new_round = Round(ID="example") # coder création et assignation d'ID

        tournament.add_round(new_round)

        return new_round

    def create_match_for_round(self, current_round: Round, players: list[Player]):
        if current_round.number == 1:
            pairs = self.create_random_pairs(players)

            for pair in pairs:
                player_1 = pair[0]
                player_2 = pair[1]
                new_match = Match(player_1, player_2)
                current_round.matchs.append(new_match)

        players_scores = []

        if current_round.number != 1:
            players_scores = self.get_players_ranking(tournament)
        



    def start_tournament():
        pass

    def shuffle_a_list(self, list_to_shuffle: list):
        shuffled_list = list_to_shuffle[:]

        if len(shuffled_list) % 2 != 0:
            raise ValueError("Number of players must be pair and at least two.")

        random.shuffle(shuffled_list)

        return shuffled_list

    def create_random_pairs(self, list_of_players: list[Player]):
        shuffled_players = self.shuffle_a_list(list_of_players)

        pairs = []

        for index in range(0, len(shuffled_players), 2):
            pair = (shuffled_players[index], shuffled_players[index + 1])
            pairs.append(pair)

        return pairs

    def get_player_score(self, player: Player, tournament: Tournament):
        total_score = 0

        for round in tournament.rounds:
            for match in round.matchs:
                if match.status == EventStatus.FINSIHED:
                    if match.white_player == player:
                        total_score += match.white_player_score
                    if match.black_player == player:
                        total_score += match.black_player_score

        return total_score

    def get_players_ranked(self, tournament: Tournament):
        ranked_players = []

        for player in tournament.players:
            total_score = self.get_player_score(player, tournament)
            ranked_players.append((player, total_score))

        ranked_players = sorted(ranked_players, key=lambda x: x[1], reverse=True)

        return ranked_players

    def have_players_already_played(
            self,
            player_1: Player,
            player_2: Player,
            list_of_rounds: list[Round]
    ):

        for round in list_of_rounds:
            for match in round.matchs:
                if (
                    (player_1 == match.player_1 and player_2 == match.player_2)
                    or
                    (player_1 == match.player_2 and player_2 == match.player_1)
                ):
                    return True

        return False

    def group_players_by_rank(self, ranked_players: list):
        players_groups = {}

        for player, score in ranked_players:
            if score not in players_groups:
                players_groups[score] = []
            players_groups[score] = player

        return players_groups

    def find_available_opponent(
            self,
            player: Player,
            list_of_players: list[Player],
            list_of_rounds: list[Round]
    ):

        for opponent in list_of_players:
            if not self.have_players_already_played(
                player,
                opponent,
                list_of_rounds
            ):
                return opponent

            return None

    def pair_players_by_score(
            self,
            ranked_players: list[tuple[Player, float]], 
            list_of_rounds: list[Round]):

        players_groups = self.group_players_by_rank(ranked_players)

        pairs = []
        leftover_players = None

        for score in sorted(players_groups, reverse=True):
            players_to_pair = players_groups[score] + leftover_players

            self.shuffle_a_list(players_to_pair)

            while len(players_to_pair) >=2:
                player_1 = players_to_pair.pop(0)

                opponent = self.find_available_opponent(
                    player_1,
                    players_to_pair,
                    list_of_rounds,
                )

                if opponent is None:
                    leftover_players.append(player_1)
                else:
                    players_to_pair.remove(opponent)
                    pairs.append((player_1, opponent))

            if len(players_to_pair) == 1:
                remaining_player = players_to_pair.pop(0)
                leftover_players.append(remaining_player)

        if leftover_players:
            if len(leftover_players) % 2 != 0:
                raise ValueError("Cannot pair an odd number of players.")

            for index in range(0, len(leftover_players), 2):
                pair =(leftover_players[index], leftover_players[index + 1])
                pairs.append(pair)

        return pairs

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
                    == start_datetime.sfrtime("%Y-%m")
                )
            ):
                return True

            return False
