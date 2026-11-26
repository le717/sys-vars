__all__ = ["SysVarNotFoundError"]


class SysVarNotFoundError(Exception):
    """A system variable was not found at `SYS_VARS_PATH`.

    Additional information about the exception may be available:
    - `var_key: str`
    - `var_type: str`
    """

    def __init__(self, *args, var_key: str = "", var_type: str = "", **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Provide some extra information about the exception
        self.var_key = var_key
        self.var_type = var_type
