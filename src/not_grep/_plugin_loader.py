"""Load not-grep checker plugins."""
from typing import Callable, Dict

import click
import pkg_resources

__all__ = ("load_plugin", "PLUGIN_ENTRY_POINT")
PLUGIN_ENTRY_POINT = "not_grep.checker"


def _load_plugins() -> Dict[str, Callable[[str, str], bool]]:
    """Load all plugins and map them by name."""

    plugins = {}  # type: Dict[str, pkg_resources.EntryPoint]

    for entry_point in pkg_resources.iter_entry_points(PLUGIN_ENTRY_POINT):
        if entry_point.name in plugins:
            raise click.exceptions.UsageError(
                f"Found conflicting entry points for '{entry_point.name}'"  # type: ignore
                "\n Registered entry points found in projects:"
                f"\n  {plugins[entry_point.name].dist.project_name}"
                f"\n  {entry_point.dist.project_name}"
            )
        plugins[entry_point.name] = entry_point

    return {name: entry_point.load() for name, entry_point in plugins.items()}


def load_plugin(name: str) -> Callable[[str, str], bool]:
    """Get the loaded plugin entry point for the requested name."""
    plugins = _load_plugins()
    try:
        return plugins[name]
    except KeyError:
        raise click.exceptions.UsageError(f"No not-grep plugin found for name '{name}'")
