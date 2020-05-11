"""Unit tests for ``not_grep._plugin_loader``."""
from collections import namedtuple

import click
import pytest
from mock import Mock

import not_grep._plugin_loader
from not_grep import checkers
from not_grep._plugin_loader import _load_plugins, load_plugin

pytestmark = [pytest.mark.local, pytest.mark.functional]


@pytest.mark.parametrize(
    "name, expected",
    (
        pytest.param("include", checkers.include, id="include"),
        pytest.param("exclude", checkers.exclude, id="exclude"),
        pytest.param("prefix", checkers.prefix, id="prefix"),
        pytest.param("suffix", checkers.suffix, id="suffix"),
        pytest.param("output-test", checkers.output_test, id="output-test"),
    ),
)
def test_load_plugin_valid(name, expected):
    test = load_plugin(name)

    assert test is expected


def test_load_plugin_duplicate(mocker):
    # "name" is a special, non-overridable attribute on mock objects
    FakeEntryPoint = namedtuple(
        "FakeEntryPoint", ["name", "module_name", "attrs", "extras", "dist"]
    )
    FakeEntryPoint.__new__.__defaults__ = (
        "MODULE",
        "ATTRS",
        "EXTRAS",
        Mock(project_name="PROJECT"),
    )

    mocker.patch.object(not_grep._plugin_loader.pkg_resources, "iter_entry_points")
    not_grep._plugin_loader.pkg_resources.iter_entry_points.return_value = [
        FakeEntryPoint(name="foo"),
        FakeEntryPoint(name="foo"),
    ]

    with pytest.raises(click.exceptions.UsageError) as excinfo:
        _load_plugins()

    excinfo.match(r"Found conflicting entry points for *")


def test_load_plugin_fail():
    with pytest.raises(click.exceptions.UsageError) as excinfo:
        load_plugin("this-will-never-exist")

    excinfo.match("No not-grep plugin found for name 'this-will-never-exist'")
