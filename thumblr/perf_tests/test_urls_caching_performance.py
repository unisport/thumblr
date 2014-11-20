from django.core.cache import get_cache
from thumblr import caching
from thumblr.dto import ImageUrlSpec
from thumblr.perf_tests.utils.profile import profile
from thumblr.perf_tests.utils.timer import timer
from thumblr.services.image_file_service import get_image_file_url
from thumblr.tests.base import BaseThumblrTestCase
from mock import patch


class TestCachingImageUrls(BaseThumblrTestCase):

    ITERATIONS = 300000

    def test_not_cached(self):
        dummy_cache = get_cache(
            'django.core.cache.backends.dummy.DummyCache'
        )
        dummy_cache.clear()

        with patch.object(caching, 'thumblr_cache', dummy_cache):
            with profile():
                with timer('Image CDN url generation. Caching DISABLED x{iters} iters.'.format(iters=self.ITERATIONS)):
                    for x in xrange(self.ITERATIONS):
                        get_image_file_url(self.image_file, ImageUrlSpec.CDN_URL)

    def test_cached(self):
        with profile():
            with timer('Image CDN url generation. Caching ENABLED x{iters} iters.'.format(iters=self.ITERATIONS)):
                for x in xrange(self.ITERATIONS):
                    get_image_file_url(self.image_file, ImageUrlSpec.CDN_URL)
