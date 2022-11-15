import json
from datetime import datetime
from os import environ, fspath
from pathlib import Path
from typing import Any, Dict, List, Optional, OrderedDict, Union

import dotenv


__all__ = [
    "get",
    "get_bool",
    "get_datetime",
    "get_float",
    "get_int",
    "get_json",
    "get_path",
    "SysVarNotFoundError",
]


class SysVarNotFoundError(Exception):
    """A system variable was not found at `SYS_VARS_PATH`.

    Additional information about the exception may be available:
    - `var_key: str`
    - `var_type: str`
    - `var_path: str`
    """

    def __init__(self, *args: object, **kwargs: Dict[str, str]) -> None:
        super().__init__(*args)

        # Provide some extra information about the exception
        self.var_key: str = kwargs.pop("key", "")
        self.var_type: str = kwargs.pop("type", "")
        self.var_path: str = fspath(globals()["__SYS_VARS_PATH"])


# Get the defined sys vars path from the environment
try:
    __SYS_VARS_PATH = Path(environ["SYS_VARS_PATH"]).resolve()
except KeyError:
    raise KeyError(
        "`SYS_VARS_PATH` could not be found in the current environment."
    ) from None

# Load the contents of a .env file.
# It's OK if it doesn't exist
__DOT_ENV_CONTENT: OrderedDict = dotenv.dotenv_values(__SYS_VARS_PATH / ".env")


def __from_directory(key: str, /) -> Optional[str]:
    """Try to find the variable in a directory."""
    try:
        return (__SYS_VARS_PATH / key).read_text().strip() or None
    except FileNotFoundError:
        return None


def __from_env(key: str, /) -> Optional[str]:
    """Try to get the variable from the environment."""
    return environ.get(key)


def __from_env_file(key: str, /) -> Optional[str]:
    """Try to get the variable from a .env file."""
    return __DOT_ENV_CONTENT.get(key)


def get(key: str, /, *, default: Optional[Any] = None, **kwargs: Dict[str, str]) -> str:
    """Get a system variable value as a str type.

    Check the value of SYS_VARS_PATH and os.environ for the key,
    preferring values from SYS_VARS_PATH. If the key
    is not found and a default value is specified,
    the default value will be returned. Otherwise,
    SysVarNotFoundError will be raised.

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
    raise SysVarNotFoundError(
        f'Could not get value for system variable "{key}"',
        key=key,
        type=kwargs.pop("var_type", "str"),
    )


def get_bool(key: str, /, **kwargs: Dict[str, Any]) -> bool:
    """Get a system variable as a bool object.

    See signature of get() for parameter details."""
    # Start by getting the system value
    sys_val = get(key, var_type="bool", **kwargs)

    # We have an actual boolean data type
    # (most likely a specified default value).
    # There's nothing we need to do for it
    if isinstance(sys_val, bool):
        return sys_val

    # We got a "word" string back, check if is an boolean word
    elif sys_val.isalpha():
        bool_strings = ("y", "yes", "t", "true")
        return sys_val.lower() in bool_strings

    # The sys val is mostly likely number, cast it
    # and check the truthy-ness of the resulting number
    else:
        sys_val = float(sys_val)
        return bool(sys_val)


def get_datetime(key: str, /, **kwargs: Dict[str, Any]) -> datetime:
    """Get a system variable as a datetime.datetime object.

    The datestring is parsed using datetime.datetime.fromisoformat(),
    and as such, expects ISO 8601 strings written using
    date.isoformat() or datetime.isoformat().

    Raises ValueError if the data cannot be cast.

    See signature of get() for parameter details."""
    sys_val = get(key, var_type="datetime", **kwargs)

    # We have an actual datetime obj (most likely a default val)
    # There's nothing more to do
    if isinstance(sys_val, datetime):
        return sys_val
    return datetime.fromisoformat(sys_val)


def get_float(key: str, /, **kwargs: Dict[str, Any]) -> float:
    """Get a system variable as a float value.

    Raises ValueError if the data cannot be cast.

    See signature of get() for parameter details."""
    return float(get(key, var_type="float", **kwargs))


def get_int(key: str, /, **kwargs: Dict[str, Any]) -> int:
    """Get a system variable as an int value.

    Raises ValueError if the data cannot be cast.

    See signature of get() for parameter details."""
    return int(get(key, var_type="int", **kwargs))


def get_json(key: str, /, **kwargs: Dict[str, Any]) -> Union[Dict[str, Any], List[Any]]:
    """Get a JSON string system variable as a dictionary object.

    Unlike the other methods whose names suggest the return data type
    of the system variable, this method refers to the type of data
    that is being retrieved. Because a raw JSON string is probably
    not too useful, the JSON string is automatically decoded into
    a Python dictionary or list for immediate consumption by the caller.
    This operates in a similar vein Flask's Request/Response get_json method.

    Raises json.JSONDecodeError if the JSON data cannot be decoded.

    See signature of get() for parameter details."""
    sys_val = get(key, var_type="json", **kwargs)

    # We have a dictionary or list (most likely a default val)
    # There's nothing more to do
    if isinstance(sys_val, dict) or isinstance(sys_val, list):
        return sys_val

    return json.loads(sys_val)


def get_path(key: str, /, **kwargs: Dict[str, Any]) -> Path:
    """Get a file path string system variable as a pathlib.Path instance.

    See signature of get() for parameter details."""
    return Path(get(key, var_type="path", **kwargs))
