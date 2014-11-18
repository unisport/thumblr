from datetime import datetime
import random
import os
import sys

import boto
from django.conf import settings
from django.core.files import File
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from moto import mock_s3

from thumblr.models import ImageSize
from thumblr.utils.hash import file_hash


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
        s3_connection = boto.connect_s3(self.aws_key, self.aws_secret)
        self.bucket_conn = s3_connection.get_bucket(self.bucket)

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

        original_file = self.bucket_conn.get_key(key_name="images/{date}/{filename}".format(
            date=datetime.today().strftime("%d-%m-%Y"),
            filename="boots.jpg"
        ))
        self.assertIsNotNone(original_file, "Original file doesn't exist on S3")

        hash_file = self.bucket_conn.get_key(key_name="images/{date}/{filename}.jpg".format(
            date=datetime.today().strftime("%d-%m-%Y"),
            filename=file_hash(File(open(self.image_file_path, 'rb')))
        ))
        self.assertIsNotNone(hash_file, "Hash file doesn't exist on S3")



