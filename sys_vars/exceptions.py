from os import fspath


__all__ = ["SysVarNotFoundError"]


class SysVarNotFoundError(Exception):
    """A system variable was not found at `SYS_VARS_PATH`.

    Additional information about the exception may be available:
    - `var_key: str`
    - `var_type: str`
    - `var_path: str`
    """

    def __init__(self, var_key: str = "", var_type: str = "") -> None:
        # Provide some extra information about the exception
        self.var_key = var_key
        self.var_type = var_type
        self.var_path: str = fspath(globals()["__SYS_VARS_PATH"])
