import click
import PySide6
from ._version import __version__  # type: ignore

from preprocessor.gui.main_window import show_application


@click.group()
def cli() -> None:
    pass


@cli.command()
def version() -> None:
    click.echo(f"CAMBioMed Preprocessor {__version__}")
    # use getattr to avoid mypy errors when stubs don't expose __version__
    pyside_ver = getattr(PySide6, "__version__", "unknown")
    qtcore_ver = getattr(getattr(PySide6, "QtCore", None), "__version__", "unknown")
    click.echo(f"  PySide6: {pyside_ver}")
    click.echo(f"  PySide6 QtCore: {qtcore_ver}")


@cli.command()
def gui() -> None:
    show_application()


def setup_logging() -> None:
    import logging

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("preprocessor")
    logger.info("Logging is set up.")


def main() -> None:
    setup_logging()
    cli()


if __name__ == "__main__":
    main()
