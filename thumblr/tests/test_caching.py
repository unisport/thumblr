from random import random
from django.core.cache import get_cache
from django.test import TestCase
from thumblr import caching
from mock import patch
from thumblr.caching import cached
from thumblr.dto import ImageUrlSpec
from thumblr.services.image_file_service import get_image_file_url
from thumblr.tests.base import BaseThumblrTestCase


@cached
def _cached_func(x, y, z):
    return random()


@cached
def _cached_func_2(x, y, z):
    return random()


class TestCaching(TestCase):

    def test_basic(self):
        locmem_cache = get_cache(
            'django.core.cache.backends.locmem.LocMemCache')
        locmem_cache.clear()

        with patch.object(caching, 'thumblr_cache', locmem_cache):
            val0 = _cached_func(2, 4, 5)
            val1 = _cached_func(1, 2, 3)
            val2 = _cached_func(1, 2, 3)
            val3 = _cached_func(2, 4, 5)

            val2_ = _cached_func_2(1, 2, 3)
            val3_ = _cached_func_2(2, 4, 5)

        self.assertEqual(val0, val3)
        self.assertEqual(val1, val2)
        self.assertNotEqual(val0, val1)
        self.assertNotEqual(val0, val2)
        self.assertNotEqual(val3, val1)
        self.assertNotEqual(val3, val2)
        self.assertNotEqual(val2, val2_)
        self.assertNotEqual(val3, val3_)


class TestCachingImageUrls(BaseThumblrTestCase):

    def test_basic(self):
        locmem_cache = get_cache(
            'django.core.cache.backends.locmem.LocMemCache')
        locmem_cache.clear()

        with patch.object(caching, 'thumblr_cache', locmem_cache):
            url1 = get_image_file_url(self.image_file, ImageUrlSpec.CDN_URL)
            url2 = get_image_file_url(self.image_file, ImageUrlSpec.CDN_URL)

        self.assertEqual(url1, url2)



