from thumblr.services.image_file_service import get_image_file_metadata, get_image_files_by_spec
from thumblr.tests.base import BaseThumblrTestCase


class TestGetImageFileMetadata(BaseThumblrTestCase):

    def test_basic(self):
        image_file = get_image_files_by_spec(self.image_metadata, one=True)

        image_file_metadata = get_image_file_metadata(image_file)

        self.assertEqual(
            image_file_metadata.is_main, False
        )

        self.assertEqual(
            image_file_metadata.content_type_id, self.image_metadata.content_type_id,
        )

        self.assertEqual(
            image_file_metadata.object_id, self.image_metadata.object_id
        )