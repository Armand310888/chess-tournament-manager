from src.views.input_helpers import (
    prompt_until_valid,
    validate_yes_or_no_string,
)


class RoundView:
    """"""

    def prompt_for_new_round(self, tournament: Tournament):
        choice = prompt_until_valid(
            "Create round? Enter 'y' for YES or 'n' for NO: ",
            validate_yes_or_no_string
        )

        return choice

