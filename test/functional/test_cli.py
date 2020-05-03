"""Black-box functional tests for the CLI."""
import os
from functools import partial

import pytest
from click.testing import CliRunner

from not_grep import cli

pytestmark = [pytest.mark.local, pytest.mark.functional]

HERE = os.path.abspath(os.path.dirname(__file__))
VECTORS_ROOT = os.path.join(HERE, "..", "vectors")


def _named_vectors(name: str):
    for dirpath, _, filenames in os.walk(VECTORS_ROOT):
        for filename in filenames:
            if filename == name:
                yield os.path.join(dirpath, filename)


_PASS_VECTORS = partial(_named_vectors, "pass.toml")
_FAIL_VECTORS = partial(_named_vectors, "fail.toml")


@pytest.mark.parametrize("filename", _PASS_VECTORS())
def test_pass_vectors(filename):
    runner = CliRunner()
    result = runner.invoke(cli, ["--config", filename, "-vvv"])
    assert result.exit_code == 0


@pytest.mark.parametrize("filename", _FAIL_VECTORS())
def test_fail_vectors(filename):
    runner = CliRunner()
    result = runner.invoke(cli, ["--config", filename, "-vvv"])
    assert result.exit_code != 0
