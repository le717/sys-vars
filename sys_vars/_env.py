__all__ = ["dot_env", "has_dot_env"]


def _fallback(*args, **kwargs) -> dict:  # ruff: ignore[unused-function-argument]
    """If python-dotenv is not installed, provide a noop method."""
    return {}


try:
    from dotenv import dotenv_values

    dot_env = dotenv_values

    has_dot_env = True
except ModuleNotFoundError:
    has_dot_env = False

    dot_env = _fallback
