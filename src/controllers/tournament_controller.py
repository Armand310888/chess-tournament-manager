
from models.tournament import Tournament
from views.tournament_view import TournamentView



class TournamentController:
    def __init__(self):
        self.tournament_view = TournamentView()

    def create_tournament(self):
        tournament_data = self.tournament_view.prompt_for_tournament()

        # attribuer un ID?
        # ajouter des joueurs?
        # ajouter des rounds?
        # définir le round en cours?

        tournament = Tournament(**tournament_data)

        return tournament
    
    def set_id(self, tournament: Tournament):

