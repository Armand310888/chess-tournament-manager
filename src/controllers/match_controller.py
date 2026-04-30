from src.models.match import Match


def create_match(white_player: Player, black_player: Player) -> Match:
    matches = load_matches() #depuis JSON
    next_id = compute_next_id(matches)

    return Match(
        white_player=white_player,
        black_player=black_player,
        match_id=next_id
    )

def load_matches():
    pass

def compute_next_id():
    pass