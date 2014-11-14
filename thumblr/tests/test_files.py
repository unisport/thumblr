import os

from django.core.files.uploadedfile import UploadedFile
from django.test import TestCase

from thumblr.files import HashedFile


class TestHashedFile(TestCase):
    def setUp(self):
        self.image_file_path = os.path.join(
            os.path.dirname(__file__), "data", "boots.jpg"
        )

    def test_basic_usage(self):
        with open(self.image_file_path) as f:
            hf = HashedFile(f, f.name)

        self.assertNotIn("boots.jpg", hf.name)
        self.assertEqual(hf.name, '4d6d69494a4f')

    def test_not_hashed_file(self):
        with open(self.image_file_path) as f:
            uf = UploadedFile(f, f.name)

        self.assertIn("boots.jpg", uf.name)
        self.assertNotEqual(uf.name, '4d6d69494a4f')