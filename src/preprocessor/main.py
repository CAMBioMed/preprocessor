from ._version import __version__
import click

@click.group()
def cli():
    pass

@cli.command()
def version():
    click.echo(f"CAMBioMed Preprocessor {__version__}")


if __name__ == "__main__":
    cli()
