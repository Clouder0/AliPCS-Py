from typing import Optional, Any
from functools import wraps


class AliPCSError(Exception):
    def __init__(self, message: str, error_code: Optional[str] = None, cause=None):
        self.__cause__ = cause
        self.error_code = error_code
        super().__init__(message)


def parse_error(error_code: str, info: Any = None) -> AliPCSError:
    msg = f"error_code: {error_code}, response: {info}"
    return AliPCSError(msg, error_code=error_code)


def assert_ok(func):
    """Assert the errno of response is not 0"""

    @wraps(func)
    def check(*args, **kwargs):
        info = func(*args, **kwargs)
        error_code = info.get("code")

        if error_code:
            err = parse_error(error_code, str(info))
            raise err

        return info

    return check


def to_refresh_token(func):
    @wraps(func)
    def refresh(*args, **kwargs):
        for _ in range(2):
            self = args[0]

            info = func(*args, **kwargs)
            if info.get("code") == "AccessTokenInvalid":
                self.refresh()
                continue
            else:
                return info

        raise parse_error("AccessTokenInvalid")

    return refresh
