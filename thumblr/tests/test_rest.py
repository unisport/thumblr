from datetime import datetime
import random
import boto
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
import os
import sys
from moto import mock_s3
from thumblr.models import ImageSize


class TestAddImageView(TestCase):
    def setUp(self):
        self.image_file_path = os.path.join(
            os.path.dirname(__file__), "data", "boots.jpg"
        )
        self.site_id = 1
        self.content_type_id = 1
        self.object_id = random.randint(0, sys.maxint)

        original_size = ImageSize(name=ImageSize.ORIGINAL)
        original_size.save()

        self.aws_key = settings.AWS_ACCESS_KEY_ID
        self.aws_secret = settings.AWS_SECRET_ACCESS_KEY
        self.bucket = settings.AWS_THUMBLR_BUCKET

    # @mock_s3
    def test_basic_addition(self):
        c = Client()

        with open(self.image_file_path) as f:
            resp = c.post(reverse("thumblr:add_image"), {
                "image": f,
                "site_id": self.site_id,
                "content_type": self.content_type_id,
                "object_id": self.object_id
            })
            self.assertEqual(resp.status_code, 200, "Add image failed")

    def test_file_in_s3(self):
        # Test doesn't make sence if mocked with @mock_s3
        c = boto.connect_s3(self.aws_key, self.aws_secret)
        bucket = c.get_bucket(self.bucket)
        original_file = bucket.get_key(key_name="images/{date}/{filename}".format(
            date=datetime.today().strftime("%d-%m-%Y"),
            filename="boots.jpg"
        ))
        self.assertIsNotNone(original_file, "Original file does't exist on S3")

