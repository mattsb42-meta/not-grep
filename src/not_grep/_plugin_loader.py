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
            existing_dist = plugins[entry_point.name].dist
            current_dist = entry_point.dist

            existing_name = existing_dist.project_name if existing_dist else "unknown"
            current_name = current_dist.project_name if current_dist else "unknown"

            raise click.exceptions.UsageError(
                f"Found conflicting entry points for '{entry_point.name}'"
                "Registered entry points found in projects:"
                f"{existing_name}"
                f"{current_name}"
            )
        plugins[entry_point.name] = entry_point

    return {name: entry_point.load() for name, entry_point in plugins.items()}


def load_plugin(name: str) -> Callable[[str, str], bool]:
    """Get the loaded plugin entry point for the requested name."""
    plugins = _load_plugins()
    try:
        return plugins[name]
    except KeyError as error:
        raise click.exceptions.UsageError(
            f"No not-grep plugin found for name '{name}'"
        ) from error
