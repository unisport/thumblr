from contextlib import contextmanager

__mocked = False


def mock_for_tests(f):
    def _f(*args, **kwargs):
        if is_mocked():
            return mock_func(*args, **kwargs)
        else:
            return f(*args, **kwargs)

    return _f


def mock_func(img, *args, **kwargs):
    print("calling mocked image processing function")
    return img


@contextmanager
def thumblr_pil_mock():
    set_mocked(True)
    yield
    set_mocked(False)


def set_mocked(flag):
    global __mocked
    __mocked = flag


def is_mocked():
    return __mocked
