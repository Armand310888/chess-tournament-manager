"""Base console view and shared display formatting helpers."""

from questionary import Style
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule


class BaseView:
    """Provide shared console display behavior for all views."""

    APP_WIDTH = 80

    QUESTIONARY_STYLE = Style([
        ("question", "bold cyan"),
        ("instruction", "italic fg:#888888"),
        ("pointer", "bold yellow"),
        ("highlighted", "fg:#b58900"),
    ])

    def __init__(self) -> None:
        """Initialize the shared Rich console."""
        self.console = Console()

    def display_application_header(self) -> None:
        """Display the application title header."""
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
        """Display a highlighted section title."""
        self.console.print(
            Rule(
                f"[bold yellow]{title}[/]",
                style="yellow",
            ),
            width=self.APP_WIDTH,
        )

    def pause(self) -> None:
        """Pause execution until the user presses Enter."""
        self.console.input("\n[yellow]Press Enter to continue...[/yellow]")

    def display_error(self, error: Exception | str) -> None:
        """Display a formatted error message."""
        self.console.print(
            self.error_format(str(error))
        )

    def clear(self) -> None:
        """Clear the console display."""
        self.console.clear()

    def display_success(self, message: str) -> None:
        """Display a formatted success message.

        Args:
            message: Success message to display.
        """
        self.console.print(
            Panel(
                f"[bold green]{message}[/bold green]",
                border_style="green",
                width=self.APP_WIDTH,
            )
        )

    @staticmethod
    def prompt_format(message: str) -> str:
        """Format a console prompt message."""
        return f"[yellow]{message}[/yellow]"

    @staticmethod
    def results_title_format(title: str) -> str:
        """Format a result section title."""
        return f"[bold yellow]{title}[/bold yellow]"

    @staticmethod
    def content_format(data_name: str, data_value: object) -> str:
        """Format a label-value line with aligned labels.

    Args:
        data_name: Label displayed before the value.
        data_value: Value associated with the label.

    Returns:
        Rich markup string ending with a newline.
    """
        return (
            f"[underline]{data_name:<30}[/underline]"
            f": {data_value}\n"
        )

    @staticmethod
    def error_format(error_message: str) -> str:
        """Display a formatted error message.

        Args:
            error: Exception or message to display.
        """

        return (
            "[bold red][underline]Error[/underline][/bold red]: "
            f"{error_message}\n"
        )
