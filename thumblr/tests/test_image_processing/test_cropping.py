import StringIO

from PIL import Image
from django.test import TestCase
import os
from thumblr.image_processing.cropping import crop_image
from thumblr.tests.base import TuplesCompareMixin
from thumblr.image_processing.basic_operations import ImagePos


class TestCropping(TestCase, TuplesCompareMixin):

    def setUp(self):
        self.image_file_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "rect_img.jpg"
        )

        file_content = None
        with open(self.image_file_path) as f:
             file_content = f.read()

        self.image_data = StringIO.StringIO(file_content)
        self.boots_pil_image = Image.open(self.image_data)

    def test_basic(self):

        res = crop_image(self.boots_pil_image, ImagePos(x=320, y=50), ImagePos(x=800, y=300))

        # self.boots_pil_image.show()
        # res.show()

        self.assertAlmostEqualTuples(
            self.boots_pil_image.getpixel((350, 100)),
            res.getpixel((30, 50)),
        )

        self.assertAlmostEqualTuples(
            self.boots_pil_image.getpixel((370, 120)),
            res.getpixel((50, 70)),
        )