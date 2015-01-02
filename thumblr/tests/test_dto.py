from django.test import TestCase
from thumblr import ImageMetadata
from thumblr.models import ImageSize


class TestImageDTO(TestCase):
    def test_extend(self):
        dto = ImageMetadata(site_id=1, content_type_id=1, object_id=1)

        updated_dto = dto.extend(content_type_id=99, size_slug=ImageSize.ORIGINAL)

        self.assertEqual(
            dto.content_type_id,
            1,
        )
        self.assertIsNone(
            dto.size_slug
        )
        self.assertEqual(
            dto.object_id,
            1,
        )

        self.assertIsInstance(updated_dto, ImageMetadata)

        self.assertEqual(updated_dto.size_slug, ImageSize.ORIGINAL)
        self.assertEqual(updated_dto.content_type_id, 99)

    def test_empty(self):
        self.assertTrue(ImageMetadata())
        self.assertTrue(ImageMetadata(site_id=1, content_type_id=1, object_id=1))
        self.assertTrue(ImageMetadata(site_id=1, content_type_id=1))
        self.assertTrue(ImageMetadata(size_slug=ImageSize.SQUARED))

