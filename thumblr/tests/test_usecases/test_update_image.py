from django.core.files import File
import os
from thumblr import usecases
from thumblr import dto
from thumblr.tests.base import BaseThumblrTestCase


class TestUpdateImageUsecase(BaseThumblrTestCase):

    def setUp(self):
        super(TestUpdateImageUsecase, self).setUp()
        self.new_image = os.path.join(
            os.path.dirname(__file__), "..", "data", "costume.jpg"
        )

    def test_basic_usage(self):
        old_s3_url = usecases.get_image_url(self.image_metadata, dto.ImageUrlSpec.S3_URL)
        old_cdn_url = usecases.get_image_url(self.image_metadata, dto.ImageUrlSpec.CDN_URL)

        with open(self.new_image) as f:
            new_image_metadata = usecases.update_image(
                File(f), self.image_metadata
            )

        assert isinstance(new_image_metadata, dto.ImageMetadata)

        self.assertNotEqual(
            new_image_metadata.image_hash,
            self.image_metadata.image_hash,
        )

        self.assertNotEqual(
            usecases.get_image_url(new_image_metadata, dto.ImageUrlSpec.S3_URL),
            old_s3_url,
        )

        self.assertNotEqual(
            usecases.get_image_url(new_image_metadata, dto.ImageUrlSpec.CDN_URL),
            old_cdn_url,
        )