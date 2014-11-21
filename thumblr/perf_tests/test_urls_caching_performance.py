import StringIO
import random
import string
from django.core.cache import get_cache
from django.core.files.base import File
from thumblr import caching
from thumblr.dto import ImageUrlSpec, ImageMetadata
from thumblr import usecases
from thumblr.models import ImageSize
from thumblr.perf_tests.utils.profile import profile
from thumblr.perf_tests.utils.timer import timer
from thumblr.services.image_file_service import get_image_file_url
from thumblr.tests.base import BaseThumblrTestCase
from mock import patch


class TestCachingImageUrls(BaseThumblrTestCase):

    TMP_FILES = 100
    ITERATIONS = 30000

    def _random_string(self):
        return ''.join(random.choice(string.ascii_lowercase) for _ in xrange(10))

    def setUp(self):
        super(TestCachingImageUrls, self).setUp()

        self.tmp_images = []
        for i in xrange(TestCachingImageUrls.TMP_FILES):
            rnd_str = self._random_string()
            f = StringIO.StringIO(rnd_str)
            _, image_file = usecases.add_image(
                File(f, rnd_str),
                ImageMetadata(
                    file_name=rnd_str,
                    size_slug=ImageSize.ORIGINAL,
                    site_id=1,
                    content_type_id=1,
                    object_id=1
                )
            )

            self.tmp_images.append(image_file)

    def test_not_cached(self):
        dummy_cache = get_cache(
            'django.core.cache.backends.dummy.DummyCache'
        )
        dummy_cache.clear()

        with patch.object(caching, 'thumblr_cache', dummy_cache):
            with profile():
                with timer('Image CDN url generation. Caching DISABLED x{iters} iters.'.format(iters=self.ITERATIONS)):
                    for i in xrange(self.ITERATIONS):
                        image_file = self.tmp_images[random.randint(0, self.TMP_FILES - 1)]
                        get_image_file_url(image_file, ImageUrlSpec.CDN_URL)

        from django.db import connection
        print(connection.queries)

    def test_cached(self):
        with profile():
            with timer('Image CDN url generation. Caching ENABLED x{iters} iters.'.format(iters=self.ITERATIONS)):
                for i in xrange(self.ITERATIONS):
                    image_file = self.tmp_images[random.randint(0, self.TMP_FILES - 1)]
                    get_image_file_url(image_file, ImageUrlSpec.CDN_URL)

        from django.db import connection
        print(connection.queries)
