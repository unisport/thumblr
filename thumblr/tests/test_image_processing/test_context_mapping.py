from PIL import Image
from thumblr.image_processing.context_mapping import get_pil_image_by_image_metadata
from thumblr.tests.base import BaseThumblrTestCase


class TestGetPilImageByImageMetadata(BaseThumblrTestCase):

    def test_basic(self):
        pil_image = get_pil_image_by_image_metadata(self.image_metadata)

        # uncomment for local testing, could be a bad thing for automated CI
        # pil_image.show()
        self.assertIsInstance(pil_image, Image.Image)
        self.assertEqual(pil_image.size, (1000, 1000))
