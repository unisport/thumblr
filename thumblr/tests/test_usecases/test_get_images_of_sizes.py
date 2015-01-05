from django.contrib.contenttypes.models import ContentType
from django.core.files import File
import os
from thumblr import usecases, ImageMetadata
from thumblr.models import ImageSize, Image
from thumblr.tests.base import BaseThumblrTestCase


class TestUpdateImageUsecase(BaseThumblrTestCase):
    content_type_id = ContentType.objects.get_for_model(Image).id

    def setUp(self):
        super(TestUpdateImageUsecase, self).setUp()

        squared = ImageSize(name=ImageSize.SQUARED, content_type_id=self.content_type_id)
        squared.save()

        self.another_image_metadata = ImageMetadata(
            file_name='costume.jpg',
            site_id=1,
            size_slug=ImageSize.SQUARED,
            content_type_id=self.content_type_id,
            object_id=1,
            is_main=True,
        )

        self.new_image = os.path.join(
            os.path.dirname(__file__), "..", "data", "costume.jpg"
        )

        with open(self.new_image) as f:
            self.another_image_metadata = usecases.add_image(
                File(f), self.another_image_metadata,
            )

    def test_basic(self):
        image_by_sizes = usecases.get_images_of_sizes(ImageMetadata(
            content_type_id=self.content_type_id,
            object_id=1,
        ))

        self.assertIsInstance(image_by_sizes, dict)
        self.assertIn(ImageSize.SQUARED, image_by_sizes)
        self.assertIn(ImageSize.ORIGINAL, image_by_sizes)
        self.assertEqual(len(image_by_sizes), 2)
