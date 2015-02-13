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

    def test_s3_url_multiple(self):
        urls = usecases.get_image_url(self.image_metadata, ImageUrlSpec.S3_URL, one=False)

        self.assertIsInstance(urls, tuple)
        self.assertIn(u"https", urls[0])
        self.assertIn(u"s3.amazonaws.com", urls[0])
        self.assertNotIn(u"boots.jpg", urls[0])

    def tearDown(self):
        Image.objects.all().delete()
        ImageSize.objects.all().delete()