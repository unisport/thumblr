import StringIO
from PIL import Image
from django.test import TestCase
import os
from thumblr.image_processing import overlaying
from mock import patch
from thumblr.tests.base import TuplesCompareMixin


class TestPutWaterMarkOnImage(TestCase, TuplesCompareMixin):

    def setUp(self):
        self.image_file_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "boots.jpg",
        )

        file_content = None
        with open(self.image_file_path) as f:
             file_content = f.read()

        self.boots_pil_image = Image.open(StringIO.StringIO(file_content))

        self.watermark_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "watermark.png",
        )

        file_content = None
        with open(self.watermark_path) as f:
             file_content = f.read()

        self.watermark = Image.open(StringIO.StringIO(file_content))

    def test_basic(self):
        with patch.object(overlaying, "get_watermark_image_for") as get_watermark_image_for__MOCK:
            get_watermark_image_for__MOCK.return_value = self.watermark

            watermarked_image = overlaying.put_watermark_on_image(self.boots_pil_image, 1)

            self.assertNotEqual(watermarked_image, self.boots_pil_image)

            self.assertEqual(watermarked_image.size, self.boots_pil_image.size)

            self.assertAlmostEqualTuples(
                watermarked_image.getpixel((
                    watermarked_image.size[0] - self.watermark.size[0] - 10,
                    watermarked_image.size[1] - self.watermark.size[1] - 10,
                )),
                self.watermark.getpixel((
                    self.watermark.size[0] - 5,
                    self.watermark.size[1] - 5,
                )),
                delta=40,
            )


class TestPutBubbleOnImage(TestCase, TuplesCompareMixin):

    def setUp(self):
        self.image_file_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "boots.jpg",
        )

        file_content = None
        with open(self.image_file_path) as f:
             file_content = f.read()

        self.boots_pil_image = Image.open(StringIO.StringIO(file_content))

        self.bubble_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "bubble_20.png",
        )

        file_content = None
        with open(self.bubble_path) as f:
             file_content = f.read()

        self.bubble = Image.open(StringIO.StringIO(file_content))

    def test_basic(self):
        with patch.object(overlaying, "get_bubble_image_for") as get_bubble_image_for__MOCK:
            get_bubble_image_for__MOCK.return_value = self.bubble

            image_with_bubble = overlaying.put_bubble_on_image(self.boots_pil_image, 20)

            self.assertNotEqual(image_with_bubble, self.boots_pil_image)

            self.assertEqual(image_with_bubble.size, self.boots_pil_image.size)

            self.assertAlmostEqualTuples(
                self.bubble.getpixel((10, 10)),
                image_with_bubble.getpixel((15, 15)),
                delta=20,
            )

