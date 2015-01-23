from django.contrib.contenttypes.models import ContentType
from django.core.files.base import File
from django.test import TestCase
import os
from thumblr import ImageMetadata, ImageUrlSpec
from thumblr.exceptions import NoSuchImageException
from thumblr.models import ImageSize, Image
from thumblr.tests.mocks import mock__add_image, mock__get_image_url, _find_image, reset_thumblr_usecases_mock, \
    mock__delete_images, mock__get_all_images, mock__update_images_metadata


class TestMockedMultipleEntries(TestCase):
    def setUp(self):
        reset_thumblr_usecases_mock()
        self.content_type_id = ContentType.objects.get_for_model(Image).id

        original_size = ImageSize(name=ImageSize.ORIGINAL, content_type_id=self.content_type_id)
        original_size.save()

        self.image_file_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "rect_img.jpg"
        )

        dto = ImageMetadata(
            file_name="rect_img.jpg",
            site_id=1,
            size_slug=ImageSize.ORIGINAL,
            content_type_id=1,
            object_id=1,
            is_main=True,
            order_number=0,
        )
        dto.extend()

        for i in range(5):
            with open(self.image_file_path) as f:
                mock__add_image(File(f), dto.extend(file_name="rect_{i}.jpg".format(i=i)))

        self.dto = dto

    def test__find_image_one(self):
        gen = _find_image(self.dto.extend(file_name="rect_1.jpg"))
        r, _ = next(gen)
        with self.assertRaises(StopIteration):
            next(gen)

    def test__find_image_many(self):
        gen = _find_image(self.dto.extend(file_name=None))
        for i in range(5):
            r, _ = next(gen)
        with self.assertRaises(StopIteration):
            next(gen)

    def test_get_image_url(self):
        url = mock__get_image_url(self.dto.extend(file_name="rect_3.jpg"), ImageUrlSpec.S3_URL)
        self.assertIn("rect_3.jpg", url)

        with self.assertRaises(NoSuchImageException):
            url = mock__get_image_url(self.dto.extend(file_name="no_such_image.jpg"), ImageUrlSpec.S3_URL)

    def test_delete_image(self):
        was = len(mock__get_all_images(self.dto.extend(file_name=None)))

        mock__delete_images(self.dto.extend(file_name="rect_3.jpg"), None)

        now = len(mock__get_all_images(self.dto.extend(file_name=None)))
        self.assertEqual(was - now, 1)

    def test_delete_image__all(self):
        was = len(mock__get_all_images(self.dto.extend(file_name=None)))

        mock__delete_images(self.dto.extend(file_name=None), None)

        now = len(mock__get_all_images(self.dto.extend(file_name=None)))
        self.assertEqual(now, 0)

    def test_delete_image__excepted(self):
        was = len(mock__get_all_images(self.dto.extend(file_name=None)))

        mock__delete_images(self.dto.extend(file_name=None), self.dto.extend(file_name="rect_3.jpg"))

        now = len(mock__get_all_images(self.dto.extend(file_name=None)))
        self.assertEqual(now, 1)

    def test_update_image_metadata(self):
        was = len(mock__get_all_images(self.dto.extend(file_name=None)))
        mock__update_images_metadata(
            self.dto.extend(file_name=None),
            self.dto.extend(file_name='XOXOXO', object_id=999)
        )

        now = len(mock__get_all_images(self.dto.extend(file_name='XOXOXO', object_id=999)))
        wrong = len(mock__get_all_images(self.dto.extend(file_name='XOXOXO', object_id=666)))

        self.assertEqual(wrong, 0)
        self.assertEqual(was, now)


class TestMockUsecases(TestCase):

    def setUp(self):
        reset_thumblr_usecases_mock()
        self.content_type_id = ContentType.objects.get_for_model(Image).id

        original_size = ImageSize(name=ImageSize.ORIGINAL, content_type_id=self.content_type_id)
        original_size.save()

        self.image_file_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "rect_img.jpg"
        )

    def test_add_image_mock(self):
        dto = ImageMetadata(
            file_name="rect_img.jpg",
            site_id=1,
            size_slug=ImageSize.ORIGINAL,
            content_type_id=1,
            object_id=1,
            is_main=True,
            order_number=0,
        )

        with open(self.image_file_path) as f:
            dto = mock__add_image(File(f), dto)

        self.assertIsNotNone(dto.image_file_id)
        self.assertIsNotNone(dto.image_hash)
        mock__get_image_url(dto, ImageUrlSpec.S3_URL)
