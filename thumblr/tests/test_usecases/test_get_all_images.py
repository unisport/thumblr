from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.test import TestCase
import os
from thumblr import usecases, ImageMetadata
from thumblr.models import ImageSize, Image
from thumblr.tests.base import BaseThumblrTestCase


class TestGetAllImagesUsecase(BaseThumblrTestCase):
    content_type_id = ContentType.objects.get_for_model(Image).id

    def setUp(self):
        super(TestGetAllImagesUsecase, self).setUp()

        squared = ImageSize(name=ImageSize.SQUARED, content_type_id=self.content_type_id)
        squared.save()

        self.another_image_metadata = ImageMetadata(
            file_name='costume.jpg',
            site_id=1,
            size_slug=ImageSize.SQUARED,
            content_type_id=self.content_type_id,
            object_id=1,
            is_main=True,
        )

        self.new_image = os.path.join(
            os.path.dirname(__file__), "..", "data", "costume.jpg"
        )

        with open(self.new_image) as f:
            self.another_image_metadata = usecases.add_image(
                File(f), self.another_image_metadata,
            )

    def test_filter_size(self):
        images_data = usecases.get_all_images(
            ImageMetadata(
                size_slug=ImageSize.ORIGINAL,
            )
        )

        self.assertEqual(len(images_data), 1)
        self.assertIsInstance(images_data[0], ImageMetadata)
        self.assertEqual(images_data[0].file_name, self.image_metadata.file_name)

        images_data = usecases.get_all_images(
            ImageMetadata(
                size_slug=ImageSize.SQUARED,
            )
        )

        self.assertEqual(len(images_data), 1)
        self.assertIsInstance(images_data[0], ImageMetadata)
        self.assertEqual(images_data[0].file_name, self.another_image_metadata.file_name)

        images_data = usecases.get_all_images(
            ImageMetadata()
        )

        self.assertEqual(len(images_data), 2)

    def test_filter_content_type(self):
        images_data = usecases.get_all_images(
            ImageMetadata(
                content_type_id=0,
            )
        )

        self.assertEqual(len(images_data), 0)

        images_data = usecases.get_all_images(
            ImageMetadata(
                content_type_id=self.content_type_id,
            )
        )

        self.assertEqual(len(images_data), 2)

    def test_filter_is_main(self):
        images_data = usecases.get_all_images(
            ImageMetadata(
                is_main=True,
            )
        )

        self.assertEqual(len(images_data), 1)

        images_data = usecases.get_all_images(
            ImageMetadata(
                is_main=False,
            )
        )

        self.assertEqual(len(images_data), 1)

    def test_filter_site_is_null(self):
        images_data = usecases.get_all_images(
            ImageMetadata(
                site_id=ImageMetadata.SITE_IS_NULL,
            )
        )

        self.assertEqual(len(images_data), 0)

        images_data = usecases.get_all_images(
            ImageMetadata()
        )

        self.assertEqual(len(images_data), 2)


class TestGetAllImagesUsecaseOrdered(TestCase):

    def setUp(self):
        super(TestGetAllImagesUsecaseOrdered, self).setUp()

        self.content_type_id = ContentType.objects.get_for_model(Image).id

        squared = ImageSize(name=ImageSize.SQUARED, content_type_id=self.content_type_id)
        squared.save()

        self.dto1 = ImageMetadata(
            file_name='costume.jpg',
            site_id=1,
            size_slug=ImageSize.SQUARED,
            content_type_id=self.content_type_id,
            object_id=1,
            is_main=True,
            order_number=1,
        )

        self.dto2 = self.dto1.extend(order_number=2)

        self.img1 = os.path.join(
            os.path.dirname(__file__), "..", "data", "costume.jpg"
        )

        self.img2 = os.path.join(
            os.path.dirname(__file__), "..", "data", "boots.jpg"
        )

        with open(self.img1) as f:
            self.dto1 = usecases.add_image(
                File(f), self.dto1,
            )

        with open(self.img2) as f:
            self.dto2 = usecases.add_image(
                File(f), self.dto2,
            )

    def test_ordered(self):
        ordered_imgs = usecases.get_all_images(
            ImageMetadata(
                content_type_id=self.content_type_id,
                object_id=1,
            ), ordered=True
        )

        self.assertEqual(len(ordered_imgs), 2)

        self.assertEqual(ordered_imgs[0].order_number, 1)
        self.assertEqual(ordered_imgs[1].order_number, 2)

        self.assertEqual(ordered_imgs[0].image_file_id, self.dto1.image_file_id)
        self.assertEqual(ordered_imgs[1].image_file_id, self.dto2.image_file_id)