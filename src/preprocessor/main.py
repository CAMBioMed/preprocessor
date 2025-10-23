from ._version import __version__
import click
import PySide6.QtCore

@click.group()
def cli():
    pass

@cli.command()
def version():
    click.echo(f"CAMBioMed Preprocessor {__version__}")
    click.echo(f"  PySide6: {PySide6.__version__}")
    click.echo(f"  PySide6 QtCore: {PySide6.QtCore.__version__}")


if __name__ == "__main__":
    cli()
