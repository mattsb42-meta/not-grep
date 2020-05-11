"""Run the checks."""
import shutil

import click

from ._config import Config

__all__ = ("run",)


def _center_pad(*, message: str, pad: str) -> str:
    columns, _lines = shutil.get_terminal_size()
    return message.center(columns, pad)


def _result_pad(*, message: str, result: str) -> str:
    columns, _lines = shutil.get_terminal_size()
    pad_char = "."
    pad_width = columns - len(message) - len(result) - 1
    return f"{message}{pad_char * pad_width} {result}"


def _check_pass(filename: str):
    click.secho(_result_pad(message=filename, result="PASS"), fg="green")


def _check_fail(filename: str):
    click.secho(_result_pad(message=filename, result="FAIL"), fg="red", err=True)


def run(*, config: Config, verbosity: int) -> bool:
    """Run all configured checks and return the desired shell exit code."""
    verbose = verbosity > 0
    all_checks_passed = True
    for checker_name, checks in config.checks.items():
        # 1. Display the checker name
        click.echo(_center_pad(message=f"Running {checker_name} checks", pad="="))
        # 2. For each check:
        for check in checks:
            # 2a. Display the check pattern
            click.echo(_center_pad(message=f"Checking {check.glob} for pattern", pad="-"))
            click.echo(check.pattern)
            click.echo(_center_pad(message="", pad="*"))
            # 2b. For each file:
            for filename in check.files():
                check_passed = check.checker(filename, check.pattern)
                # 2b1. Display result
                if not check_passed:
                    _check_fail(filename)
                elif verbose:
                    _check_pass(filename)
                all_checks_passed = all_checks_passed and check_passed

    return all_checks_passed
