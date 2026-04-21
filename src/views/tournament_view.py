

class TournamentView:
    def prompt_for_tournament(self):
        name = input(
            "Enter the tournament's name : "
        )
        place = input(
            "Enter the tournament address : "
        )
        start_date = input(
            "Enter the tournament starting date and time : "
        )
        end_date = input(
            "Enter the tournament end date and time : "
        )
        number_of_players = input(
            "Enter the maximum number of players admitted to the tournament : "
        )
        number_of_rounds = input(
            "Enter the tournament number of rounds (by default: 4) : "
        )
        description = input(
            "Enter the tournament description : "
        )

        return {
            "name": name,
            "place": place,
            "start_date": start_date,
            "end_date": end_date,
            "number_of_players": number_of_players,
            "number_of_rounds": number_of_rounds,
            "description": description
        }
