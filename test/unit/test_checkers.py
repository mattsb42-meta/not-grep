"""Unit tests for ``not_grep.checkers``."""
from typing import Dict

import pytest

from not_grep import checkers
from not_grep._config import Config, SingleCheck

pytestmark = [pytest.mark.local, pytest.mark.functional]

PREFIX_PATTERN = "prefix pattern"
SUFFIX_PATTERN = "suffix pattern"
INCLUDE_PATTERN = "include pattern"
EXCLUDE_PATTERN = "exclude pattern"


@pytest.fixture
def source_file(tmpdir) -> str:
    source = tmpdir.join("source")
    source.write(f"""{PREFIX_PATTERN}
    more data
    {INCLUDE_PATTERN}
    more data
    {SUFFIX_PATTERN}""")
    return str(source)


@pytest.mark.parametrize("check, pattern", (
    pytest.param(checkers.include, INCLUDE_PATTERN, id="include"),
    pytest.param(checkers.exclude, EXCLUDE_PATTERN, id="exclude"),
    pytest.param(checkers.prefix, PREFIX_PATTERN, id="prefix"),
    pytest.param(checkers.suffix, SUFFIX_PATTERN, id="suffix"),
    pytest.param(checkers.output_test, "pass", id="output-test"),
))
def test_checkers_pass(source_file, check, pattern):
    assert check(source_file, pattern)


@pytest.mark.parametrize("check, pattern", (
    pytest.param(checkers.include, EXCLUDE_PATTERN, id="include"),
    pytest.param(checkers.exclude, INCLUDE_PATTERN, id="exclude"),
    pytest.param(checkers.prefix, EXCLUDE_PATTERN, id="prefix not present"),
    pytest.param(checkers.prefix, INCLUDE_PATTERN, id="prefix present but not prefix"),
    pytest.param(checkers.suffix, EXCLUDE_PATTERN, id="suffix not present"),
    pytest.param(checkers.suffix, INCLUDE_PATTERN, id="suffix present but not suffix"),
    pytest.param(checkers.output_test, "foo", id="output-test"),
))
def test_checkers_fail(source_file, check, pattern):
    assert not check(source_file, pattern)
