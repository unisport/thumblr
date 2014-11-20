import StringIO
import cProfile
from contextlib import contextmanager
import pstats


@contextmanager
def profile():
    pr = cProfile.Profile()
    pr.enable()

    yield

    pr.disable()
    s = StringIO.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print s.getvalue()
