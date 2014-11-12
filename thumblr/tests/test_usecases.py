from django.test import TestCase
import os
from thumblr.dto import ImageMetadataDTO
from thumblr.usecases import add_image


class TestAddImageUseCase(TestCase):

    def setUp(self):
        self.image_file_path = os.path.join(
            os.path.dirname(__file__), "data", "boots.jpg"
        )

    def test_basic_addition(self):

        image_metadata = ImageMetadataDTO(
            file_name="boots.jpg",
            file_type="Rectangle",
            site_id=None,
            content_type_id=None,
            object_id=None,
        )

        with open(self.image_file_path) as f:
            add_image(f, image_metadata)
