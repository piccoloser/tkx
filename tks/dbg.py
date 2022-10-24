from functools import wraps
from os import environ


def dbg(return_values: bool):
    """
    Decorator assigned to a function in order to view
    its positional and keyword arguments when called.
    Only works when the DEBUG environment variable is
    equal to "true".

    Arguments:
    * `return_values`: If `True`, print the result of
    the input function.
    """

    def outer(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            env_debug = environ.get("DEBUG") == "true"
            if env_debug:
                print(
                    f"{fn.__qualname__}"
                    f"({', '.join(map(str, args))}, "
                    f"{', '.join(map(lambda i: f'{i[0]}={i[1]}', kwargs.items()))})"
                )

            result = fn(*args, **kwargs)

            if env_debug and return_values:
                print(f"\t-> {result}")

            return result

        return inner

    return outer
