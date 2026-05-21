""""""
from src.views.base_view import BaseView
from src.views.input_helpers import (
    prompt_until_valid,
    validate_yes_or_no_string,
    OptionalOrNot,
)
from src.models.round import Round


class RoundView(BaseView):
    """"""
    def prompt_for_new_round(self):
        choice = prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            self.prompt_format(
                "Create round? (y/n) : "
            ),
            validate_yes_or_no_string,
            console=self.console
        )

        return choice

    def display_created_round(self, new_round: Round) -> None:
        """"""
        content = (
            self.results_title_format("New Round created successfully")
            + self.content_format("Round number", new_round.number)
        )

        self.console.print(content)
