from django.core.files import File
from moto import mock_s3
import os
from thumblr.dto import ImageMetadata
from thumblr.models import ImageSize
from thumblr.tests.base import BaseThumblrTestCase
from thumblr.usecases import delete_images, add_image, get_all_images


class TestDeleteImagesUsecase(BaseThumblrTestCase):

    def setUp(self):
        super(TestDeleteImagesUsecase, self).setUp()

        squared = ImageSize(name=ImageSize.SQUARED, content_type_id=2)
        squared.save()

        self.another_image_metadata = ImageMetadata(
            file_name='costume.jpg',
            site_id=1,
            size_slug=ImageSize.SQUARED,
            content_type_id=self.content_type_id,
            object_id=2,
            is_main=True,
        )

        self.new_image = os.path.join(
            os.path.dirname(__file__), "..", "data", "costume.jpg"
        )

        with open(self.new_image) as f:
            self.another_image_metadata = add_image(
                File(f), self.another_image_metadata,
            )

    def test_delete_all(self):
        imgs = get_all_images(ImageMetadata())
        self.assertEqual(len(imgs), 2)

        delete_images(ImageMetadata())

        imgs = get_all_images(ImageMetadata())
        self.assertEqual(len(imgs), 0)

    def test_delete_by_related_object(self):
        imgs = get_all_images(ImageMetadata())
        self.assertEqual(len(imgs), 2)

        delete_images(ImageMetadata(
            content_type_id=self.content_type_id,
            object_id=1,
        ))

        imgs = get_all_images(ImageMetadata())
        self.assertEqual(len(imgs), 1)

    def test_delete_by_related_object_except(self):
        imgs = get_all_images(ImageMetadata())
        self.assertEqual(len(imgs), 2)

        delete_images(
            ImageMetadata(
                content_type_id=self.content_type_id,
                object_id=2,
            ), excepted=ImageMetadata(
                content_type_id=self.content_type_id,
                object_id=2,
                size_slug=ImageSize.ORIGINAL,
            )
        )

        imgs = get_all_images(ImageMetadata())
        self.assertEqual(len(imgs), 1)

    def test_delete_by_related_object_except_2(self):
        imgs = get_all_images(ImageMetadata())
        self.assertEqual(len(imgs), 2)

        delete_images(
            ImageMetadata(
                content_type_id=self.content_type_id,
                object_id=2,
            ),
            excepted=ImageMetadata(
                content_type_id=self.content_type_id,
                object_id=2,
                size_slug=ImageSize.SQUARED,
            ),
        )

        imgs = get_all_images(ImageMetadata())
        self.assertEqual(len(imgs), 2)

    def test_delete_by_related_object_except_all(self):
        imgs = get_all_images(ImageMetadata())
        self.assertEqual(len(imgs), 2)

        delete_images(
            ImageMetadata(),
            excepted=ImageMetadata(),
        )

        imgs = get_all_images(ImageMetadata())
        self.assertEqual(len(imgs), 2)

    def test_delete_by_related_object_except_miss(self):
        imgs = get_all_images(ImageMetadata())
        self.assertEqual(len(imgs), 2)

        delete_images(
            ImageMetadata(),
            excepted=ImageMetadata(site_id=99999),
        )

        imgs = get_all_images(ImageMetadata())
        self.assertEqual(len(imgs), 0)

    def test_delete_by_size(self):
        imgs = get_all_images(ImageMetadata())
        self.assertEqual(len(imgs), 2)

        delete_images(ImageMetadata(
            size_slug=ImageSize.SQUARED,
        ))

        imgs = get_all_images(ImageMetadata())
        self.assertEqual(len(imgs), 1)

    def test_delete_except_multi(self):
        imgs = get_all_images(ImageMetadata())
        self.assertEqual(len(imgs), 2)

        delete_images(ImageMetadata(), [
            ImageMetadata(size_slug=ImageSize.SQUARED,),
            ImageMetadata(size_slug=ImageSize.ORIGINAL,)
        ])

        imgs = get_all_images(ImageMetadata())
        self.assertEqual(len(imgs), 2)
