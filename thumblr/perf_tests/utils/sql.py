from contextlib import contextmanager
from django.db import connection


@contextmanager
def log_sql(verbose=False):
    """
    Requires DEBUG = True, some test runner set it to False automatically
    """
    start = len(connection.queries)

    yield

    end = len(connection.queries)

    print("SQL LOG (TOTAL QUERIES={total})".format(total=end-start))

    if verbose:
        for q in connection.queries[start:end]:
            print(q)
