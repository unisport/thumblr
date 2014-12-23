from django.core.files import File
import os
from thumblr import usecases, ImageMetadata
from thumblr.models import ImageSize
from thumblr.tests.base import BaseThumblrTestCase


class TestUpdateImageUsecase(BaseThumblrTestCase):

    def setUp(self):
        super(TestUpdateImageUsecase, self).setUp()

        squared = ImageSize(name=ImageSize.SQUARED)
        squared.save()

        self.another_image_metadata = ImageMetadata(
            file_name='costume.jpg',
            site_id=1,
            size_slug=ImageSize.SQUARED,
            content_type_id=1,
            object_id=1,
        )

        self.new_image = os.path.join(
            os.path.dirname(__file__), "..", "data", "costume.jpg"
        )

        with open(self.new_image) as f:
            self.another_image_metadata = usecases.add_image(
                File(f), self.another_image_metadata,
            )

    def test_filter_size(self):
        images_data = usecases.get_all_images(
            ImageMetadata(
                size_slug=ImageSize.ORIGINAL,
            )
        )

        self.assertEqual(len(images_data), 1)
        self.assertIsInstance(images_data[0], ImageMetadata)
        self.assertEqual(images_data[0].original_file_name, self.image_metadata.original_file_name)

        images_data = usecases.get_all_images(
            ImageMetadata(
                size_slug=ImageSize.SQUARED,
            )
        )

        self.assertEqual(len(images_data), 1)
        self.assertIsInstance(images_data[0], ImageMetadata)
        self.assertEqual(images_data[0].original_file_name, self.another_image_metadata.original_file_name)

        images_data = usecases.get_all_images(
            ImageMetadata()
        )

        self.assertEqual(len(images_data), 2)

    def test_filter_content_type(self):
        images_data = usecases.get_all_images(
            ImageMetadata(
                content_type_id=0,
            )
        )

        self.assertEqual(len(images_data), 0)

        images_data = usecases.get_all_images(
            ImageMetadata(
                content_type_id=1,
            )
        )

        self.assertEqual(len(images_data), 2)
