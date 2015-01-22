
from django.test.runner import DiscoverRunner
from moto import mock_s3


class ThumblrTestRunner(DiscoverRunner):
    """
    DiscoverRunner
    """
    def setup_test_environment(self, *args, **kwargs):
        self.s3_mock = mock_s3()
        self.s3_mock.__enter__()
        super(ThumblrTestRunner, self).setup_test_environment(*args, **kwargs)

    def teardown_test_environment(self, *args, **kwargs):
        self.s3_mock.__exit__()
        super(ThumblrTestRunner, self).teardown_test_environment(*args, **kwargs)
