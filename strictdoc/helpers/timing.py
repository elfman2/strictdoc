import contextlib
from functools import wraps
from time import time

from strictdoc.helpers.math import round_up


def timing_decorator(name):
    def timing_internal(func):
        @wraps(func)
        def wrap(*args, **kw):
            print(f"Step '{name}' start", flush=True)  # noqa: T201
            time_start = time()
            result = func(*args, **kw)
            time_end = time()
            print(  # noqa: T201
                f"Step '{name}' took: {round_up(time_end - time_start, 2)} sec",
                flush=True,
            )
            return result

        return wrap

    return timing_internal


@contextlib.contextmanager
def measure_performance(title):
    time_start = time()
    yield
    time_end = time()

    time_diff = time_end - time_start
    padded_name = f"{title} ".ljust(60, ".")
    padded_time = " {:0.2f}".format(  # pylint: disable=consider-using-f-string
        time_diff
    ).rjust(6, ".")
    print(f"{padded_name}{padded_time}s", flush=True)  # noqa: T201
