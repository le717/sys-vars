from datetime import datetime
from pathlib import Path
from typing import Any
from warnings import warn

from ._core import SysVars


__all__ = ["get", "get_bool", "get_datetime", "get_float", "get_int", "get_json", "get_path"]


# Internal instance of class
__sys_vars = SysVars()


def get(key: str, /, *, default: Any | None = None) -> str:
    """Get a system variable value as a str type.

     TODO: duplicated docstring from class!

    Check the value of `SYS_VARS_PATH` and `os.environ` for the key, preferring values
    from `SYS_VARS_PATH`. If the key is not found and a default value is specified,
    the default value will be returned. Otherwise, `SysVarNotFoundError` will be raised.

    @param key - The system variable key.
    @param default - A default value is the key is not found.
    @return - The system variable value.
    """
    warn(
        "`sys_vars.get()` is deprecated. Please switch to the class-based API.", DeprecationWarning
    )
    return __sys_vars.get(key, default=default)


def get_bool(key: str, /, *, default: Any | None = None) -> bool:
    """Get a system variable as a `bool` object.

    See signature of `get()` for full parameter details.
    """
    warn(
        "`sys_vars.get_bool()` is deprecated. Please switch to the class-based API.",
        DeprecationWarning,
    )
    return __sys_vars.get_bool(key, default=default)


def get_datetime(key: str, /, *, default: Any | None = None) -> datetime:
    """Get a system variable as a `datetime.datetime` object.

    The datestring is parsed using `datetime.datetime.fromisoformat()`,
    and as such, expects ISO 8601 strings written using
    `date.isoformat()` or `datetime.isoformat()`.

    Raises `ValueError` if the data cannot be cast.

    See signature of `get()` for full parameter details.
    """
    warn(
        "`sys_vars.get_datetime()` is deprecated. Please switch to the class-based API.",
        DeprecationWarning,
    )
    return __sys_vars.get_datetime(key, default=default)


def get_float(key: str, /, *, default: Any | None = None) -> float:
    """Get a system variable as a `float` value.

    Raises `ValueError` if the data cannot be cast.

    See signature of `get()` for full parameter details.
    """
    warn(
        "`sys_vars.get_float()` is deprecated. Please switch to the class-based API.",
        DeprecationWarning,
    )
    return __sys_vars.get_float(key, default=default)


def get_int(key: str, /, *, default: Any | None = None) -> int:
    """Get a system variable as an `int` value.

    Raises `ValueError` if the data cannot be cast.

    See signature of `get()` for full parameter details.
    """
    warn(
        "`sys_vars.get_int()` is deprecated. Please switch to the class-based API.",
        DeprecationWarning,
    )
    return __sys_vars.get_int(key, default=default)


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
    warn(
        "`sys_vars.get_json()` is deprecated. Please switch to the class-based API.",
        DeprecationWarning,
    )
    return __sys_vars.get_json(key, default=default)


def get_path(key: str, /, *, default: Any | None = None) -> Path:
    """Get a file path string system variable as a `pathlib.Path` instance.

    See signature of `get()` for full parameter details.
    """
    warn(
        "`sys_vars.get_path()` is deprecated. Please switch to the class-based API.",
        DeprecationWarning,
    )
    return __sys_vars.get_path(key, default=default)
