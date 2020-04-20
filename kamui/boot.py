from kamui.application import create_app
from kamui.configuration.database import init_db

application = create_app()


@application.cli.command("initdb")
def _init_db() -> None:
    init_db()


if __name__ == "__main__":
    application.run()
