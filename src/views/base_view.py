""""""
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.align import Align
from questionary import Style


class BaseView:
    """"""
    APP_WIDTH = 80

    QUESTIONARY_STYLE = Style([
        ("question", "bold cyan"),
        ("instruction", "italic fg:#888888"),
        ("pointer", "bold yellow"),
        ("highlighted", "fg:#b58900"),
    ])

    def __init__(self) -> None:
        self.console = Console()

    def display_application_header(self) -> None:
        self.console.print()
        self.console.print(
            Panel(
                Align.center(
                    "[bold cyan]Chess Tournament Manager[/]"
                ),
                width=self.APP_WIDTH,
                border_style="cyan"
            )
        )

    def display_section_title(self, title: str) -> None:
        self.console.print(
            Rule(
                f"[bold yellow]{title}[/]",
                style="yellow"
            ),
            width=self.APP_WIDTH,
        )

    def pause(self) -> None:
        """"""
        self.console.input("\n[yellow]Press Enter to continue...[/yellow]")

    def display_error(self, error_message: str) -> None:
        """Display a formatted error message."""

        self.console.print(
            self.error_format(error_message)
        )

    @staticmethod
    def prompt_format(message: str) -> str:
        """"""
        return f"[yellow]{message}[/yellow]"

    @staticmethod
    def results_title_format(title: str) -> str:
        """"""
        return f"[bold yellow]{title}[/bold yellow]"

    @staticmethod
    def content_format(data_name: str, data_value: str) -> str:
        """"""
        return (
            f"[underline]{data_name:<30}[/underline]"
            f": {data_value}\n"
        )

    @staticmethod
    def error_format(error_message: str) -> str:
        """Format an error message."""

        return (
            "[bold red][underline]Error[/underline][/bold red]: "
            f"{error_message}\n"
        )
