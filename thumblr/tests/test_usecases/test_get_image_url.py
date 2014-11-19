from mock import patch
from moto import mock_s3
from thumblr.dto import ImageUrlSpec
from thumblr.models import ImageSize, Image
from thumblr import usecases
from thumblr.tests.base import BaseThumblrTestCase


class TestGetImageUrl(BaseThumblrTestCase):

    def test_path_only_url(self):
        url = usecases.get_image_url(self.image_metadata, ImageUrlSpec.PATH_ONLY_URL)

        self.assertNotIn(u"http", url)
        self.assertNotIn(u"boots.jpg", url)

    def test_s3_url(self):
        url = usecases.get_image_url(self.image_metadata, ImageUrlSpec.S3_URL)

        self.assertIn(u"https", url)
        self.assertIn(u"s3.amazonaws.com", url)
        self.assertNotIn(u"boots.jpg", url)

    def test_cdn_url(self):
        url = usecases.get_image_url(self.image_metadata, ImageUrlSpec.CDN_URL)

        self.assertIn(u"http", url)
        self.assertIn(u"static", url)
        self.assertIn(u"unisport.dk", url)
        self.assertNotIn(u"boots.jpg", url)

    def tearDown(self):
        Image.objects.all().delete()
        ImageSize.objects.all().delete()