import StringIO

from PIL import Image
from django.test import TestCase
import os
from thumblr.image_processing import basic_operations
from thumblr.tests.base import TuplesCompareMixin
from thumblr.image_processing.basic_operations import ImageDim, ImagePos


class TestSquarify(TestCase, TuplesCompareMixin):

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
        squared_image = basic_operations.squarify(
            self.boots_pil_image,
            result_size=ImageDim(width=1000, height=1000)
        )

        squared_etalon = Image.open(os.path.join(
            os.path.dirname(__file__), "..", "data", "squared_img.jpg"
        ))

        # uncomment for local testing, could be a bad thing for automated CI
        # squared_etalon.show()
        # squared_image.show()

        # No side effect, no change to image in parameter
        self.assertNotEqual(
            self.boots_pil_image.size,
            squared_image.size
        )

        self.assertEqual(
            squared_image.size,
            squared_etalon.size,
        )

        for x in xrange(10, 900, 50):
            for y in xrange(10, 420, 50):
                self.assertAlmostEqualTuples(
                    squared_image.getpixel((x, y)),
                    squared_etalon.getpixel((x, y)),
                    delta=25,  # means: more or less colors are the same
                )


class TestOverlay(TestCase, TuplesCompareMixin):

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

        self.squared_thumbnail = basic_operations.squarify(
            squared_etalon,
            ImageDim(width=100, height=100)
        )

    def test_basic(self):

        result_image = basic_operations.overlay(
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

        # verify same size and some key pixels colors
        self.assertEqual(
            self.boots_pil_image.size,
            result_image.size,
        )

        self.assertAlmostEqualTuples(
            self.boots_pil_image.getpixel((450, 250)),
            result_image.getpixel((450, 250)),
            delta=5,
        )

        self.assertAlmostEqualTuples(
            self.squared_thumbnail.getpixel((50, 50)),
            result_image.getpixel((100, 100)),
            delta=5,
        )


class TestThumbnail(TestCase, TuplesCompareMixin):

    def setUp(self):
        self.image_file_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "rect_img.jpg"
        )

        file_content = None
        with open(self.image_file_path) as f:
             file_content = f.read()

        self.image_data = StringIO.StringIO(file_content)
        self.boots_pil_image = Image.open(self.image_data)

        self.thumbnail_etalon = Image.open(os.path.join(
            os.path.dirname(__file__), "..", "data", "rect_img_thumbnail_100x100.jpg"
        ))

    def test_basic(self):
        thumbnail = basic_operations.thumbnail(
            self.boots_pil_image,
            ImageDim(width=100, height=100)
        )

        # thumbnail.show()

        self.assertEqual(
            thumbnail.size,
            self.thumbnail_etalon.size
        )

        for x in xrange(5, thumbnail.size[0], 10):
            for y in xrange(5, thumbnail.size[1], 10):
                self.assertAlmostEqualTuples(
                    thumbnail.getpixel((x, y)),
                    self.thumbnail_etalon.getpixel((x, y)),
                    delta=30,  # the smaller thumbnail => the bigger color deviation
                )

