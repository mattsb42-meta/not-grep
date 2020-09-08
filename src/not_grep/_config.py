"""Parse a config file."""
import glob
from typing import Callable, Iterable, Mapping, Sequence

import attr
import toml

from ._plugin_loader import load_plugin

__all__ = ("Config", "SingleCheck")


@attr.s(auto_attribs=True)
class SingleCheck:
    """Container for information needed to run a single check."""

    checker: Callable[[str, str], bool]
    glob: str
    pattern: str

    def files(self) -> Iterable[str]:
        """Find all of the files identified by the glob."""
        return glob.glob(self.glob, recursive=True)


@attr.s(auto_attribs=True)
class Config:
    """not-grep configuration container and parser."""

    checks: Mapping[str, Sequence[SingleCheck]]

    @classmethod
    def parse(cls, config_file_path: str) -> "Config":
        """Parse a config file and load the requested checks."""
        # 1. Parse config file
        with open(config_file_path, "r") as config_file:
            parsed = toml.load(config_file)
        # 2. For each checker:
        all_checks = {}
        for checker_name, checks in parsed.items():
            # 2a. Load the checker plugin
            checker_module = load_plugin(checker_name)
            # 2b. Add a check for the plugin for each requested glob and pattern.
            all_checks[checker_name] = [
                SingleCheck(
                    checker=checker_module,
                    glob=glob_pattern,
                    pattern=check_pattern,
                )
                for glob_pattern, check_pattern in checks.items()
            ]
        return Config(checks=all_checks)
