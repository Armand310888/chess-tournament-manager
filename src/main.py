from src.controllers.main_controller import MainController


def main() -> None:
    app = MainController()
    app.run()


if __name__ == "__main__":
    main()
