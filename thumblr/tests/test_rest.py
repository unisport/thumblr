import random
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
import os
import sys
from moto import mock_s3


class TestAddImageView(TestCase):
    def setUp(self):
        self.image_file_path = os.path.join(
            os.path.dirname(__file__), "data", "boots.jpg"
        )
        self.site_id = 1
        self.object_id = random.randint(0, sys.maxint)

    @mock_s3
    def test_basic_addition(self):
        c = Client()

        with open(self.image_file_path) as f:
            resp = c.post(reverse("thumblr:add_image"), {
                "image": f,
                "site_id": self.site_id,
                "content_type": "article",
                "object_id": self.object_id
            })
            self.assertEqual(resp.status_code, 200, "Add image failed")

