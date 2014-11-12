from django.test import TestCase
import os
from thumblr.usecases import add_image


class TestAddImageUseCase(TestCase):

    def setUp(self):
        self.image_file_path = os.path.join(
            os.path.dirname(__file__), "data", "boots.jpg"
        )

    def test_basic_addition(self):
        with open(self.image_file_path) as f:
            add_image(f)
