

class TournamentView:
    def create_tournament(self):
        name = input(
            "Saissisez le nom du tournoi : "
        )
        place = input(
            "Saisissez l'adresse du tournoi : "
        )


        



        self.name = name
        self.place = place
        self.number_of_rounds = number_of_rounds
        self.actual_round = actual_round
        self.list_of_rounds = list_of_rounds
        self.list_of_players = list_of_players
        self.description = description
        self.tournament_id: int | None = None