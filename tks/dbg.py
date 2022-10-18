from os import environ


def dbg(fn):
    """
    Decorator assigned to a function in order to view
    its positional and keyword arguments when called.
    Only works when the DEBUG environment variable is
    equal to "true".
    """

    def wrapper(*args, **kwargs):
        if environ.get("DEBUG") == "true":
            print(
                f"{fn.__qualname__}"
                f"({', '.join(map(str, args))}, "
                f"{', '.join(map(lambda i: f'{i[0]}={i[1]}', kwargs.items()))})"
            )

        return fn(*args, **kwargs)

    return wrapper
