from django.core.files import File
import os
from thumblr.usecases import update_images_metadata, get_all_images, add_image
from thumblr.dto import ImageMetadata
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
            is_main=True,
        )

        self.new_image = os.path.join(
            os.path.dirname(__file__), "..", "data", "costume.jpg"
        )

        with open(self.new_image) as f:
            self.another_image_metadata = add_image(
                File(f), self.another_image_metadata,
            )

    def test_size_update(self):
        sq_images = get_all_images(
            ImageMetadata(size_slug=ImageSize.SQUARED)
        )

        self.assertEqual(len(sq_images), 1)

        update_images_metadata(
            ImageMetadata(size_slug=ImageSize.ORIGINAL),
            ImageMetadata(size_slug=ImageSize.SQUARED)
        )

        sq_images = get_all_images(
            ImageMetadata(size_slug=ImageSize.SQUARED)
        )
        self.assertEqual(len(sq_images), 2)

    def test_several_updates(self):
        sq_images = get_all_images(
            ImageMetadata()
        )

        self.assertEqual(len(sq_images), 2)

        update_images_metadata(
            ImageMetadata(),
            ImageMetadata(
                size_slug=ImageSize.SQUARED,
                object_id=2,
                content_type_id=2,
            )
        )

        sq_images = get_all_images(
            ImageMetadata(
                size_slug=ImageSize.SQUARED,
                object_id=2,
                content_type_id=2,
            )
        )
        self.assertEqual(len(sq_images), 2)
