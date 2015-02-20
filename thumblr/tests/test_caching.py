from random import random
from django.core.cache import get_cache
from django.core.files import File
from django.test import TestCase
import os
from thumblr import caching
from mock import patch
from thumblr.caching import cached, drop_cache_for
from thumblr.dto import ImageUrlSpec
from thumblr import usecases
from thumblr.tests.base import BaseThumblrTestCase


@cached
def _cached_func(x, y, z):
    return random()


@cached
def _cached_func_2(x, y, z):
    return random()


class TestCaching(TestCase):

    def test_basic(self):
        locmem_cache = get_cache('django.core.cache.backends.locmem.LocMemCache')
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


class TestDropCacheFor(TestCase):

    def test_basic(self):
        locmem_cache = get_cache('django.core.cache.backends.locmem.LocMemCache')
        locmem_cache.clear()

        with patch.object(caching, 'thumblr_cache', locmem_cache):
            val245 = _cached_func(2, 4, 5)
            val123 = _cached_func(1, 2, 3)

            drop_cache_for(_cached_func, 1, 2, 3)

            val123_ = _cached_func(1, 2, 3)
            val245_ = _cached_func(2, 4, 5)

            self.assertEqual(val245, val245_)
            self.assertNotEqual(val123, val123_)


class TestCachingImageUrls(BaseThumblrTestCase):

    def test_basic(self):
        locmem_cache = get_cache('django.core.cache.backends.locmem.LocMemCache')
        locmem_cache.clear()

        with patch.object(caching, 'thumblr_cache', locmem_cache):
            url1 = usecases.get_image_url(self.image_metadata, ImageUrlSpec.CDN_URL)
            url2 = usecases.get_image_url(self.image_metadata, ImageUrlSpec.CDN_URL)

        self.assertEqual(url1, url2)

    def test_multiple(self):
        locmem_cache = get_cache('django.core.cache.backends.locmem.LocMemCache')
        locmem_cache.clear()

        with patch.object(caching, 'thumblr_cache', locmem_cache):
            url1 = usecases.get_image_url(self.image_metadata, ImageUrlSpec.CDN_URL, one=False)
            url2 = usecases.get_image_url(self.image_metadata, ImageUrlSpec.CDN_URL, one=False)

        self.assertEqual(url1, url2)


class TestDropCacheImageUrls(BaseThumblrTestCase):

    def setUp(self):
        super(TestDropCacheImageUrls, self).setUp()
        self.new_image_file_path = os.path.join(
            os.path.dirname(__file__), "data", "costume.jpg"
        )

    def test_basic(self):
        locmem_cache = get_cache('django.core.cache.backends.locmem.LocMemCache')
        locmem_cache.clear()

        with patch.object(caching, 'thumblr_cache', locmem_cache):
            url1 = usecases.get_image_url(self.image_metadata, ImageUrlSpec.CDN_URL)

            with open(self.new_image_file_path) as f:
                self.image_file = usecases.update_image(
                    File(f),
                    self.image_metadata
                )

            url2 = usecases.get_image_url(self.image_metadata, ImageUrlSpec.CDN_URL)

        self.assertNotEqual(url1, url2)

    def test_dto_for_size_and_content_type(self):
        locmem_cache = get_cache('django.core.cache.backends.locmem.LocMemCache')
        locmem_cache.clear()

        with patch.object(caching, 'thumblr_cache', locmem_cache):
            url1 = usecases.get_image_url(
                self.image_metadata.extend(image_file_id=None, file_name=None, image_hash=None),
                ImageUrlSpec.CDN_URL
            )

            with open(self.new_image_file_path) as f:
                self.image_file = usecases.update_image(
                    File(f),
                    self.image_metadata
                )

            url2 = usecases.get_image_url(
                self.image_metadata.extend(image_file_id=None, file_name=None, image_hash=None),
                ImageUrlSpec.CDN_URL
            )

        self.assertNotEqual(url1, url2)

    def test_multiple(self):
        locmem_cache = get_cache('django.core.cache.backends.locmem.LocMemCache')
        locmem_cache.clear()

        with patch.object(caching, 'thumblr_cache', locmem_cache):
            url1 = usecases.get_image_url(self.image_metadata, ImageUrlSpec.CDN_URL, one=False)

            with open(self.new_image_file_path) as f:
                self.image_file = usecases.update_image(
                    File(f),
                    self.image_metadata
                )

            url2 = usecases.get_image_url(self.image_metadata, ImageUrlSpec.CDN_URL, one=False)

        self.assertNotEqual(url1, url2)
