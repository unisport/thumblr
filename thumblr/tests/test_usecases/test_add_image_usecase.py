import boto
from django.conf import settings
from thumblr.models import upload_to
from thumblr.tests.base import BaseThumblrTestCase


class TestAddImageUsecase(BaseThumblrTestCase):

    def setUp(self):
        super(TestAddImageUsecase, self).setUp()

        self.aws_key = settings.AWS_ACCESS_KEY_ID
        self.aws_secret = settings.AWS_SECRET_ACCESS_KEY
        self.bucket = settings.AWS_THUMBLR_BUCKET
        s3_connection = boto.connect_s3(self.aws_key, self.aws_secret)
        self.bucket_conn = s3_connection.get_bucket(self.bucket)

    def test_basic_addition(self):
        original_file = self.bucket_conn.get_key(
            key_name=upload_to(self.image_file, "boots.jpg")
        )
        self.assertIsNotNone(original_file, "Original file does't exist on S3")

        hash_file = self.bucket_conn.get_key(
            key_name=upload_to(self.image_file, "boots.jpg")
        )
        self.assertIsNotNone(hash_file, "Hash file does't exist on S3")


