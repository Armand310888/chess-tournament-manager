
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
    
    # comment créer l'ID? Fonction à part? Possible de manière automatique? Depuis la base de données?
    def assign_tournament_id(self, tournament: Tournament):
        pass

    def inscribe_players():
        pass

    def start_tournament():
        pass

    def create_next_round():
        pass

    def set_current_round():
        pass

