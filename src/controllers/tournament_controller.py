import random

from models.tournament import Tournament
from models.round import Round
from models.player import Player
from models.match import Match
from views.tournament_view import TournamentView
from views.round_view import RoundView
from models.lifecycle import EventStatus


class TournamentController:
    def __init__(self):
        self.tournament_view = TournamentView()
        self.round_view = RoundView()

    def create_tournament(self):
        tournament_data = self.tournament_view.prompt_for_tournament()

        tournament = Tournament(**tournament_data)

        return tournament

    # comment créer l'ID? Fonction à part? Possible de manière automatique? Depuis la base de données?
    def assign_tournament_id(self, tournament: Tournament):
        pass

    def select_players(self, tournament: Tournament):

        if not isinstance(tournament, Tournament):
            raise TypeError("'tournament' must be a Tournament object")

        selected_players = self.tournament_view.prompt_to_select_players

        for player in selected_players:
            tournament.add_player(player)

    def create_new_round(self, tournament: Tournament):
        choice = self.round_view.prompt_for_new_round()

        if choice != "y":
            return None

        new_round = Round(ID="example") # coder création et assignation d'ID

        tournament.add_round(new_round)

        return new_round

    def create_match_for_round(self, current_round: Round, list_of_players: list[Players]):
        if current_round.number == 1:
            pairs = self.create_random_pairs(list_of_players)

            for pair in pairs:
                player_1 = pair[0]
                player_2 = pair[1]
                new_match = Match(player_1, player_2)
                current_round.list_of_matchs.append(new_match)

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

        for round in tournament.list_of_rounds:
            for match in round.list_of_matchs:
                if match.status == EventStatus.FINSIHED:
                    if match.white_player == player:
                        total_score += match.white_player_score
                    if match.black_player == player:
                        total_score += match.black_player_score

        return total_score

    def get_players_ranked(self, tournament: Tournament):
        ranked_players = []

        for player in tournament.list_of_players:
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
            for match in round.list_of_matchs:
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
