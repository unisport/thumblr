import StringIO
from PIL import Image
from django.test import TestCase
import os
from thumblr.utils import pil_processing
from thumblr.utils.pil_processing import ImageDim, ImagePos


class TestSquarify(TestCase):

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
        squared_image = pil_processing.squarify(
            self.boots_pil_image,
            result_size=ImageDim(width=1000, height=1000)
        )

        squared_etalon = Image.open(os.path.join(
            os.path.dirname(__file__), "..", "data", "squared_img.jpg"
        ))

        # uncomment for local testing, could be a bad thing for automated CI
        # if squared_image.size != squared_etalon.size:
        #     squared_etalon.show()
        #     squared_image.show()

        # No side effect, no change to image in parameter
        self.assertNotEqual(
            self.boots_pil_image.size,
            squared_image.size
        )

        # Result image have correct size, TODO: needed more clever image comparision to etalon
        self.assertEqual(
            squared_image.size,
            squared_etalon.size,
        )


class TestOverlay(TestCase):

    def setUp(self):
        self.image_file_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "rect_img.jpg"
        )

        file_content = None
        with open(self.image_file_path) as f:
             file_content = f.read()

        self.image_data = StringIO.StringIO(file_content)
        self.boots_pil_image = Image.open(self.image_data)

        squared_etalon = Image.open(os.path.join(
            os.path.dirname(__file__), "..", "data", "squared_img.jpg"
        ))

        self.squared_thumbnail = pil_processing.squarify(
            squared_etalon,
            ImageDim(width=100, height=100)
        )

    def test_basic(self):

        result_image = pil_processing.overlay(
            self.boots_pil_image, self.squared_thumbnail,
            ImagePos(x=50, y=50),
        )

        # uncomment to check result for local testing, could be a bad thing for automated CI
        # result_image.show()

        # No side effect, no change to image in parameter
        self.assertNotEqual(
            self.boots_pil_image,
            result_image,
        )
        self.assertNotEqual(
            self.boots_pil_image,
            self.squared_thumbnail,
        )

        # stupid test, need more clever thing
        self.assertEqual(
            self.boots_pil_image.size,
            result_image.size,
        )
