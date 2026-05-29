"""Application entry point."""

from src.controllers.main_controller import MainController


def main() -> None:
    """Instantiate and run the main application controller."""
    app = MainController()
    app.run()


if __name__ == "__main__":
    main()
