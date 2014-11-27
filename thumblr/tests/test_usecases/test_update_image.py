from django.core.files import File
import os
from thumblr import usecases
from thumblr.models import ImageFile
from thumblr.tests.base import BaseThumblrTestCase


class TestUpdateImageUsecase(BaseThumblrTestCase):

    def setUp(self):
        super(TestUpdateImageUsecase, self).setUp()
        self.new_image = os.path.join(
            os.path.dirname(__file__), "..", "data", "costume.jpg"
        )

    def test_basic_usage(self):
        with open(self.new_image) as f:
            image_file = usecases.update_image(
                File(f), self.image_metadata
            )

        assert isinstance(image_file, ImageFile)

        self.assertNotEqual(
            image_file.image_hash,
            self.image_file.image_hash
        )

        self.assertNotEqual(
            image_file.image_in_storage.url,
            self.image_file.image_in_storage.url,
        )

        self.assertNotEqual(
            image_file.image_hash_in_storage.url,
            self.image_file.image_hash_in_storage.url,
        )