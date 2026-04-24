
from datetime import datetime

from models.tournament import Tournament
from models.round import Round
from views.tournament_view import TournamentView
from views.round_view import RoundView




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
        # coder le fait de ne pas pouvoir créer un round si le précédent n'est pas clôturé
        for round in tournament.list_of_rounds:
            if round.end_datetime is None:
                raise ValueError()

        choice = self.round_view.prompt_for_new_round()

        if choice != "y":
            return None
        round_number = len(tournament.list_of_rounds) + 1

        new_round = Round(
            number=round_number,
            start_datetime=datetime.now(),
            list_of_players=tournament.list_of_players
        )

        tournament.list_of_rounds.append(new_round)

        return new_round

   


    def start_tournament():
        pass

    def set_current_round():
        pass

