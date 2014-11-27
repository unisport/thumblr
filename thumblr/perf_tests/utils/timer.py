from contextlib import contextmanager
import time


@contextmanager
def timer(message=''):
    start = time.time()

    yield

    end = time.time()
    summary = (end - start)

    print("{message} Time elapsed (sec): {res_time}".format(
        message=message,
        res_time=round(summary, 8),
    ))
