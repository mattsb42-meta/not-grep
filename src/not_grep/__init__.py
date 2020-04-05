"""``not-grep`` is kind of like grep, but not quite the same."""
from typing import IO

import click

from ._config import Config
from ._run_checks import run

__all__ = ("__version__", "cli")

__version__ = "0.0.1"


@click.command()
@click.option(
    "-c", "--config", required=True, type=click.File(mode="r"), help="Path to config file"
)
@click.option("-v", "--verbose", count=True)
@click.version_option(version=f"not-grep version {__version__}")
def cli(config: IO, verbose: int):
    """not-grep is kind of like grep, but not quite the same.

    It runs checks against files based on a configuration file.
    For more information, see https://not-grep.readthedocs.io
    """
    parsed_config = Config.parse(config)
    success = run(config=parsed_config, verbosity=verbose)
    if not success:
        raise click.ClickException("Checks failed!")
