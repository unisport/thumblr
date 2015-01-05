from PIL import Image
from django.core.files import File
from django.test import TestCase
import os
from thumblr.dto import ImageMetadata
from thumblr.models import ImageSize
from thumblr.usecases import add_image
from thumblr.image_processing.context_mapping import get_pil_image_by_image_metadata, get_django_file_from_pil_image
from thumblr.tests.base import BaseThumblrTestCase
from thumblr.models import Image as ThumlrImage


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
        original_size = ImageSize.objects.create(name=ImageSize.ORIGINAL, content_type_id=1)

    def test_basic(self):
        # self.pil_image.show()

        res = get_django_file_from_pil_image(self.pil_image)

        self.assertIsInstance(res, File)

    def test_save_to_imagefield(self):
        res = get_django_file_from_pil_image(self.pil_image)

        img = add_image(res, ImageMetadata(
            file_name='boots.jpg',
            site_id=None,
            size_slug=ImageSize.ORIGINAL,
            content_type_id=1,
            object_id=1,
        ))

        im = ThumlrImage.objects.first()

        im.image_hash_in_storage.url  # this reference should not raise exception

