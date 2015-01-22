from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.test.testcases import TestCase
from moto import mock_s3
import os
from thumblr import ImageMetadata, add_image
from thumblr.models import ImageSize, Image


class TestAddImageUsecase(TestCase):

    def setUp(self):
        super(TestAddImageUsecase, self).setUp()

        self.image_file_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "boots.jpg"
        )
        self.site_id = 1
        self.content_type_id = ContentType.objects.get_for_model(Image).id
        self.object_id = 1

        original_size = ImageSize(name=ImageSize.ORIGINAL, content_type_id=self.content_type_id)
        original_size.save()

        self.image_metadata = ImageMetadata(
            file_name='boots.jpg',
            site_id=1,
            size_slug=ImageSize.ORIGINAL,
            content_type_id=self.content_type_id,
            object_id=1,
        )

    def test_basic_addition(self):
        with open(self.image_file_path) as f:
            self.image_metadata = add_image(
                File(f),
                self.image_metadata
            )

        self.assertEqual(Image.objects.count(), 1)


