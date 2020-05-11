"""Unit tests for ``not_grep._config``."""
from typing import Dict

import pytest

import not_grep._config
from not_grep import checkers
from not_grep._config import Config, SingleCheck

pytestmark = [pytest.mark.local, pytest.mark.functional]


def test_singlecheck_files(mocker):
    mocker.patch.object(not_grep._config.glob, "glob")
    check = SingleCheck(checker=lambda x, y: True, glob="foo", pattern="bar")

    test = check.files()

    not_grep._config.glob.glob.assert_called_once_with("foo", recursive=True)
    assert test is not_grep._config.glob.glob.return_value


def _config_test_cases():
    yield (
        """
        [include]
        "src/**/*.py" = "include value"

        [exclude]
        "docs/**/*.rst" = "antidisestablishmentarianism"

        [output-test]
        "*.rst" = "pass"
        "**/*.py" = "fail"

        [prefix]
        "*.md" = "my awesome prefix"

        [suffix]
        "*.rst" = "\\n"
        """,
        {
            "include": [
                SingleCheck(
                    checker=checkers.include, glob="src/**/*.py", pattern="include value"
                )
            ],
            "exclude": [
                SingleCheck(
                    checker=checkers.exclude,
                    glob="docs/**/*.rst",
                    pattern="antidisestablishmentarianism",
                )
            ],
            "output-test": [
                SingleCheck(checker=checkers.output_test, glob="*.rst", pattern="pass"),
                SingleCheck(checker=checkers.output_test, glob="**/*.py", pattern="fail"),
            ],
            "prefix": [
                SingleCheck(
                    checker=checkers.prefix, glob="*.md", pattern="my awesome prefix"
                )
            ],
            "suffix": [SingleCheck(checker=checkers.suffix, glob="*.rst", pattern="\n")],
        },
    )


@pytest.mark.parametrize("contents, mapping", _config_test_cases())
def test_config_parse(tmpdir, contents: str, mapping: Dict[str, Config]):
    source = tmpdir.join("source")
    source.write(contents)

    test = Config.parse(str(source))

    assert test.checks == mapping
