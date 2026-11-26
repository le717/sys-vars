import json
from datetime import date, datetime
from decimal import Decimal
from os import environ
from pathlib import Path
from typing import Any

from ._env import dot_env
from .exceptions import SysVarNotFoundError


__all__ = ["SysVars"]

# Get the defined sys vars path from the environment
try:
    __SYS_VARS_PATH = Path(environ["SYS_VARS_PATH"]).resolve()
except KeyError:
    msg = "`SYS_VARS_PATH` could not be found in the current environment."
    raise KeyError(msg) from None

# Load the contents of a .env file. It's OK if it doesn't exist
__DOT_ENV_CONTENT = dot_env(__SYS_VARS_PATH / ".env")


def __from_directory(key: str, /) -> str | None:
    """Try to find the variable in a directory."""
    try:
        return (__SYS_VARS_PATH / key).read_text().strip() or None
    except FileNotFoundError:
        return None


def __from_env(key: str, /) -> str | None:
    """Try to get the variable from the environment."""
    return environ.get(key)


def __from_env_file(key: str, /) -> str | None:
    """Try to get the variable from a `.env` file."""
    return __DOT_ENV_CONTENT.get(key)


class SysVars:
    """Access system variables in your code as native Python data types.


    TODO: `.env` support
    TODO: `.env` data will be loaded at init
    """

    def __init__(self, p: Path | None = None, /) -> None:
        """TODO: write me!"""
        self.__sys_vars_path: Path | None = p
        self.__known_vars: dict[str, Any] = {}
        self.set_path(p)

    def _from_directory(self, key: str, /) -> str | None:
        """Try to find the given variable in the sys vars path."""
        # In the unlikely event the sys vars path is still a `NoneType`, shortcut
        if self.__sys_vars_path is None:
            return None
        try:
            return (self.__sys_vars_path / key).read_text().strip() or None
        except FileNotFoundError:
            return None

    @staticmethod
    def _from_env(key: str, /) -> str | None:
        """Try to get the given variable from the environment."""
        return environ.get(key)

    def _load_dot_env(self) -> None:
        """Load the contents of a `.env` file. It's OK if it doesn't exist."""
        # The sys vars path is very unlikely to be a NoneType at this point, but it is possible,
        # so handle that edge case
        vals = {} if self.__sys_vars_path is None else dot_env(self.__sys_vars_path / ".env")
        self.__known_vars.update(vals)

    def reload(self) -> None:
        """TODO: write me!"""
        self.__known_vars.clear()
        self._load_dot_env()
        return None

    def set_path(self, p: Path | None = None, /) -> None:
        """Set the source path to use for retrieving variables from a file.

        The path is also used to locate a `.env` file that could contain variables, if `.env`
        support is available.

        If a specific path is not available, the `SYS_VARS_PATH` environment variable will be used.
        If that is not set, a `KeyError` exception wil be raised.
        """
        # If a path is provided, use it
        if p is not None:
            self.__sys_vars_path = p.resolve()
            return None

        # Get the defined path from the environment
        try:
            self.__sys_vars_path = Path(environ["SYS_VARS_PATH"]).resolve()
        except KeyError:
            msg = "The environment variable 'SYS_VARS_PATH' could not be found."
            raise KeyError(msg) from None

    def get(self, key: str, /, *, default: Any | None = None, __var_type: str = "str") -> str:
        """Get a system variable value as a `str` value.

        TODO: revise docstring!

        Check the value of `SYS_VARS_PATH` and `os.environ` for the key, preferring values
        from `SYS_VARS_PATH`. If the key is not found and a default value is specified,
        the default value will be returned. Otherwise, `SysVarNotFoundError` will be raised.

        :param key - The system variable key.
        :param default - A default value is the key is not found.
        :return - The system variable value.
        """
        # First check the known keys, then our sys vars path directory, falling back to the env
        var_value = self.__known_vars.get(key)
        if var_value is None:
            var_value = __from_directory(key)
        if var_value is None:
            var_value = __from_env(key)

        # We have a value, store it for quicker next time lookups before providing it to the caller
        if var_value is not None:
            var_value = var_value.strip()
            self.__known_vars[key] = var_value.strip()
            return var_value

        # We couldn't find the variable anywhere, try to send back a default value
        if default is not None:
            return default

        # No default value was given, so raise an exception
        msg = f"Could not get value for system variable {key!r}"
        raise SysVarNotFoundError(msg, var_key=key, var_type=__var_type)

    def get_bool(self, key: str, /, *, default: Any | None = None) -> bool:
        """Get a system variable as a `bool` object.

        See signature of `get()` for full parameter details.
        """

    def get_date(self, key: str, /, *, default: Any | None = None) -> date:
        """Get a system variable as a `datetime.date` object.

        The date string is parsed using `datetime.dat.fromisoformat()`,
        and as such, expects ISO 8601 strings written using
        `date.isoformat()`.

        Raises `ValueError` if the data cannot be cast.

        See signature of `get()` for full parameter details.
        """

    def get_datetime(self, key: str, /, *, default: Any | None = None) -> datetime:
        """Get a system variable as a `datetime.datetime` object.

        The datetime string is parsed using `datetime.datetime.fromisoformat()`,
        and as such, expects ISO 8601 strings written using
        `date.isoformat()` or `datetime.isoformat()`.

        Raises `ValueError` if the data cannot be cast.

        See signature of `get()` for full parameter details.
        """

    def get_decimal(self, key: str, /, *, default: Any | None = None) -> Decimal:
        """Get a system variable as a `Decimal` instance.

        See signature of `get()` for full parameter details.
        """

    def get_float(self, key: str, /, *, default: Any | None = None) -> float:
        """Get a system variable as a `float` value.

        Raises `ValueError` if the data cannot be cast.

        See signature of `get()` for full parameter details.
        """

    def get_int(self, key: str, /, *, default: Any | None = None) -> int:
        """Get a system variable as an `int` value.

        Raises `ValueError` if the data cannot be cast.

        See signature of `get()` for full parameter details.
        """

    def get_json(self, key: str, /, *, default: Any | None = None) -> dict[str, Any] | list[Any]:
        """Get a JSON string system variable as a `dict` or `list`.

        Unlike the other methods whose names suggest the return data type  of the system variable,
        this method refers to the type of data that is being retrieved. Because a raw JSON string is
        probably not too useful, the JSON string is automatically decoded into a Python dictionary
        or list for immediate consumption by the caller. This operates in a similar vein of
        Flask's Request/Response `get_json()` method.

        Raises `json.JSONDecodeError` if the JSON data cannot be decoded.

        See signature of `get()` for full parameter details.
        """

    def get_path(self, key: str, /, *, default: Any | None = None) -> Path:
        """Get a file path string system variable as a `pathlib.Path` instance.

        See signature of `get()` for full parameter details.
        """


def get(key: str, /, *, default: Any | None = None, __var_type: str = "str") -> str:
    """Get a system variable value as a str type.

    Check the value of `SYS_VARS_PATH` and `os.environ` for the key, preferring values
    from `SYS_VARS_PATH`. If the key is not found and a default value is specified,
    the default value will be returned. Otherwise, `SysVarNotFoundError` will be raised.

    @param key - The system variable key.
    @param default - A default value is the key is not found.
    @return - The system variable value.
    """
    # First check a directory, falling back to the environment
    var_value = __from_directory(key)
    if var_value is None:
        var_value = __from_env(key)
    if var_value is None:
        var_value = __from_env_file(key)

    # We have a value, send it back
    if var_value is not None:
        return var_value.strip()

    # We couldn't find the variable anywhere, try to send back a default value
    if default is not None:
        return default

    # No default value was given, so raise an exception
    msg = f"Could not get value for system variable {key!r}"
    raise SysVarNotFoundError(msg, var_key=key, var_type=__var_type)


def get_bool(key: str, /, *, default: Any | None = None) -> bool:
    """Get a system variable as a `bool` object.

    See signature of `get()` for full parameter details.
    """
    # Start by getting the system value
    sys_val = get(key, default=default, __var_type="bool")

    # We have an actual boolean data type
    # (most likely a specified default value).
    # There's nothing we need to do for it
    if isinstance(sys_val, bool):
        return sys_val

    # We got a "word" string back, check if is an boolean word
    if sys_val.isalpha():
        bool_strings = ("y", "yes", "t", "true")
        return sys_val.lower() in bool_strings

    # The sys val is mostly likely number, cast it
    # and check the truthy-ness of the resulting number
    sys_val = float(sys_val)
    return bool(sys_val)


def get_datetime(key: str, /, *, default: Any | None = None) -> datetime:
    """Get a system variable as a `datetime.datetime` object.

    The datestring is parsed using `datetime.datetime.fromisoformat()`,
    and as such, expects ISO 8601 strings written using
    `date.isoformat()` or `datetime.isoformat()`.

    Raises `ValueError` if the data cannot be cast.

    See signature of `get()` for full parameter details.
    """
    sys_val = get(key, default=default, __var_type="datetime")

    # We have an actual datetime obj (most likely a default val)
    # There's nothing more to do
    if isinstance(sys_val, datetime):
        return sys_val
    return datetime.fromisoformat(sys_val)


def get_float(key: str, /, *, default: Any | None = None) -> float:
    """Get a system variable as a `float` value.

    Raises `ValueError` if the data cannot be cast.

    See signature of `get()` for full parameter details.
    """
    return float(get(key, default=default, __var_type="float"))


def get_int(key: str, /, *, default: Any | None = None) -> int:
    """Get a system variable as an `int` value.

    Raises `ValueError` if the data cannot be cast.

    See signature of `get()` for full parameter details.
    """
    return int(get(key, default=default, __var_type="int"))


def get_json(key: str, /, *, default: Any | None = None) -> dict[str, Any] | list[Any]:
    """Get a JSON string system variable as a `dict` object.

    Unlike the other methods whose names suggest the return data type
    of the system variable, this method refers to the type of data
    that is being retrieved. Because a raw JSON string is probably
    not too useful, the JSON string is automatically decoded into
    a Python dictionary or list for immediate consumption by the caller.
    This operates in a similar vein Flask's Request/Response `get_json()` method.

    Raises `json.JSONDecodeError` if the JSON data cannot be decoded.

    See signature of `get()` for full parameter details.
    """
    sys_val = get(key, default=default, __var_type="json")

    # We have a dictionary or list (most likely a default val)
    # There's nothing more to do
    if isinstance(sys_val, (dict, list)):
        return sys_val

    return json.loads(sys_val)


def get_path(key: str, /, *, default: Any | None = None) -> Path:
    """Get a file path string system variable as a `pathlib.Path` instance.

    See signature of `get()` for full parameter details.
    """
    return Path(get(key, default=default, __var_type="path"))
