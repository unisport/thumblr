from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.test import TestCase
from moto import mock_s3
import os
from thumblr import usecases
from thumblr.dto import ImageMetadata
from thumblr.models import ImageSize, Image


# hack mocking with moto multiple times doesn't work, so mock once
s3_mock = mock_s3()
s3_mock.__enter__()


class BaseThumblrTestCase(TestCase):

    def setUp(self):
        self.image_file_path = os.path.join(
            os.path.dirname(__file__), "data", "boots.jpg"
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

        with open(self.image_file_path) as f:
            self.image_metadata = usecases.add_image(
                File(f),
                self.image_metadata
            )

    def tearDown(self):
        Image.objects.all().delete()
        ImageSize.objects.all().delete()


class TuplesCompareMixin(object):

    def assertAlmostEqualTuples(self, a, b, delta=1):
        for x, y in zip(a, b):
            self.assertAlmostEqual(x, y, delta=delta)
