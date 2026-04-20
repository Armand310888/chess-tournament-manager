

class PlayerView:
    def prompt_for_player(self):
        first_name = input(
            "Entrez le prénom du joueur : "
            )
        last_name = input(
            "Entrez le nom de famille du joueur : "
            )
        birth_date = input(
            "Entrez la date de naissance du joueur : "
            )
        elo_rating = input(
            "Entrez le classement ELO du joueur: "
            )
        chess_national_id = input(
            "Entrez l'identifiant national d'échecs du joueur: "
            )

        return {
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_date,
            "elo_rating": elo_rating,
            "chess_national_id": chess_national_id
        }
