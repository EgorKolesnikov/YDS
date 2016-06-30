import sys
import functools


def takes(*decorator_args):
    def my_decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            for arg, check in zip(decorator_args, args):
                if not isinstance(check, arg):
                    raise TypeError
            return func(*args, **kwargs)
        return wrapped
    return my_decorator

exec(sys.stdin.read())
