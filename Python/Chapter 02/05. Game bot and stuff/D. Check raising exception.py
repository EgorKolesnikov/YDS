import sys
import functools


class AssertRaises:
    def __init__(self, exception):
        self.exception = exception

    def __enter__(self):
        return self.exception

    def __exit__(self, exception_type, exception_val, trace):
        if exception_type is not None:
            if isinstance(exception_val, self.exception):
                return True
        raise AssertionError

exec(sys.stdin.read())
