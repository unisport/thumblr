from django.core.files import File
from django.test import TestCase
from moto import mock_s3
import os
from thumblr.dto import ImageMetadata, ImageUrlSpec
from thumblr.models import ImageSize
from thumblr import usecases


class TestGetImageUrl(TestCase):

    def setUp(self):
        self.image_file_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "boots.jpg"
        )
        self.site_id = 1
        self.content_type_id = 1
        self.object_id = 1

        original_size = ImageSize(name=ImageSize.ORIGINAL)
        original_size.save()

        self.image_metadata = ImageMetadata(
            file_name='boots.jpg',
            site_id=1,
            size_slug=ImageSize.ORIGINAL,
            content_type_id=1,
            object_id=1,
        )

        with open(self.image_file_path) as f:
            usecases.add_image(
                File(f),
                self.image_metadata
            )

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
