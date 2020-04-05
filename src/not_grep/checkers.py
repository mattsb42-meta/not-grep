"""Built-in checkers."""
__all__ = ("present", "not_present", "output_test")


def present(filename: str, pattern: str) -> bool:
    """Check that ``pattern`` is present in ``filename``."""
    with open(filename, "r") as data:
        return pattern in data.read()


def not_present(filename: str, pattern: str) -> bool:
    """Check that ``pattern`` is not present in ``filename``."""
    return not present(filename, pattern)


def output_test(filename: str, pattern: str) -> bool:  # pylint: disable=unused-argument
    """Test the output.

    Always passes if ``pattern == "pass"``. Otherwise, fails.
    """
    return pattern == "pass"
