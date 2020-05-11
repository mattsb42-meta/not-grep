"""Built-in checkers."""
__all__ = ("include", "exclude", "output_test")


def include(filename: str, pattern: str) -> bool:
    """Check that ``pattern`` is include in ``filename``."""
    with open(filename, "rb") as data:
        return pattern in data.read().decode("utf-8")


def exclude(filename: str, pattern: str) -> bool:
    """Check that ``pattern`` is not include in ``filename``."""
    return not include(filename, pattern)


def output_test(filename: str, pattern: str) -> bool:  # pylint: disable=unused-argument
    """Test the output.

    Always passes if ``pattern == "pass"``. Otherwise, fails.
    """
    return pattern == "pass"


def prefix(filename: str, pattern: str) -> bool:
    """Check that ``filename`` starts with ``pattern``."""
    with open(filename, "rb") as data:
        data_prefix = data.read(len(pattern))
        return data_prefix.decode("utf-8") == pattern


def suffix(filename: str, pattern: str) -> bool:
    """Check that ``filename`` ends with ``pattern``."""
    offset = -1 * len(pattern)
    with open(filename, "rb") as data:
        data.seek(offset, 2)
        data_suffix = data.read(len(pattern))
        return data_suffix.decode("utf-8") == pattern
