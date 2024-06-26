# sys-vars

> Access system variables in your code as native Python data types.

## Usage

Requires Python 3.8+

Load system variables for used in applications as secrets, variables, and other related contexts as
native Python data types. Searches for a file in `SYS_VARS_PATH`, falling back to `os.enviorn`.
If the package is installed with the `dotenv` extra (`pip install sys-vars[dotenv]`), there is a
final check in the contents of a `.env` file located in `SYS_VARS_PATH`, if one exists.

`SYS_VARS_PATH` must be a defined OS environment variable that is set
before app start. If it is not found, a `KeyError` exception will be raised.


```python
import sys_vars


# Returns <class 'str'>
# Default values can be specified if the key is missing
sys_vars.get("HOST_ADDRESS", default="localhost")

# Returns <class 'bool'>
# Default values are supported for casting methods too
# Also treats "t", "true", "y", "yes" as True value
sys_vars.get_bool("DEBUG_MODE", default=False)

# Returns <class 'datetime.datetime'>
sys_vars.get_datetime("LAST_SYNC_RUN")

# Returns <class 'float'>
sys_vars.get_float("pi")

# Returns <class 'int'>
sys_vars.get_int("THE_MEANING_OF_LIFE")

# Returns <class 'dict'> or <class 'list'>
# Automatically decodes JSON strings into dictionaries/lists
sys_vars.get_json("CONFIGURED_TERMS")

# Returns <class 'pathlib.Path'>
sys_vars.get_path("CONFIG_PATH")

# Raises `sys_vars.SysVarNotFoundError`
sys_vars.get("DOES_NOT_EXIST")
```

## Building

1. Install [Poetry](https://python-poetry.org/) 1.6.0+
1. Run `poetry install`
1. Run `poetry build`
1. Tests can be run via the provided VS Code test runner config.

The resulting `.whl` file will be located at
`./dist/sys_vars-<x.y.z>-py3-none-any.whl`
