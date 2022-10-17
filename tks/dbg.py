from os import environ


def dbg(fn):
    def wrapper(*args, **kwargs):
        if environ.get("DEBUG") == "true":
            print(
                f"{fn.__qualname__}"
                f"({', '.join(map(str, args))}, "
                f"{', '.join(map(lambda i: f'{i[0]}={i[1]}', kwargs.items()))})"
            )

        return fn(*args, **kwargs)

    return wrapper
