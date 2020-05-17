"""``not-grep`` is kind of like grep, but not quite the same."""
import os
from typing import Optional

import click

from ._config import Config
from ._run_checks import run

__all__ = ("__version__", "cli")

__version__ = "1.0.0"
_DEBUG = "INPUT_DEBUG"
_CONFIG_FILE = "INPUT_CONFIG-FILE"


@click.command()
@click.option(
    "-c",
    "--config",
    default=None,
    required=False,
    type=click.Path(
        exists=True, file_okay=True, dir_okay=False, resolve_path=True, readable=True
    ),
    help="Path to config file",
)
@click.option("-v", "--verbose", count=True)
@click.version_option(version=f"not-grep version {__version__}")
def cli(config: Optional[str], verbose: int):
    """not-grep is kind of like grep, but not quite the same.

    It runs checks against files based on a configuration file.
    For more information, see https://not-grep.readthedocs.io
    """
    if _DEBUG in os.environ:
        verbose += 1

    if config is None:
        try:
            config = os.environ[_CONFIG_FILE]
        except KeyError:
            raise click.exceptions.BadOptionUsage(
                option_name="config",
                message=f"Config file must provided or set through environment '{_CONFIG_FILE}' variable",
            )
        if not os.path.isfile(config):
            raise click.BadOptionUsage(
                option_name="config",
                message=f"Requested config file '{config}' does not exist or is not a file",
            )

    parsed_config = Config.parse(config)
    success = run(config=parsed_config, verbosity=verbose)
    if not success:
        raise click.ClickException("Checks failed!")
