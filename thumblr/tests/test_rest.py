from django.core.urlresolvers import reverse
from django.test import TestCase, Client
import os
from thumblr.models import ImageType


class TestAddImageView(TestCase):

    def setUp(self):
        self.image_file_path = os.path.join(
            os.path.dirname(__file__), "data", "boots.jpg"
        )

    def test_basic_addition(self):
        c = Client()

        with open(self.image_file_path) as f:
            resp = c.post(reverse("thumblr:add_image"), {
                "image_type": ImageType.ORIGINAL,
                "image": f,
            })
