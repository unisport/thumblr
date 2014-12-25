from PIL import Image
from django.core.files import File
from django.test import TestCase
import os
from thumblr.image_processing.context_mapping import get_pil_image_by_image_metadata, get_django_file_from_pil_image
from thumblr.tests.base import BaseThumblrTestCase


class TestGetPilImageByImageMetadata(BaseThumblrTestCase):

    def test_basic(self):
        pil_image = get_pil_image_by_image_metadata(self.image_metadata)

        # uncomment for local testing, could be a bad thing for automated CI
        # pil_image.show()
        self.assertIsInstance(pil_image, Image.Image)
        self.assertEqual(pil_image.size, (1000, 1000))


class TestGetDjangoFileFromPilImage(TestCase):

    def setUp(self):
        self.image_file_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "boots.jpg"
        )

        self.pil_image = Image.open(self.image_file_path)

    def test_basic(self):
        # self.pil_image.show()

        res = get_django_file_from_pil_image(self.pil_image)

        self.assertIsInstance(res, File)
