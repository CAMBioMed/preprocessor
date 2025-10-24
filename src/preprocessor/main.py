import click
import PySide6.QtCore
from preprocessor._version import __version__
from preprocessor.hello_world import show_ui


@click.group()
def cli():
    pass

@cli.command()
def version():
    click.echo(f"CAMBioMed Preprocessor {__version__}")
    click.echo(f"  PySide6: {PySide6.__version__}")
    click.echo(f"  PySide6 QtCore: {PySide6.QtCore.__version__}")

@cli.command()
def ui():
    show_ui()

if __name__ == "__main__":
    cli()
