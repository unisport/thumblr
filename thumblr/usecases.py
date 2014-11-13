from thumblr.dto import ImageMetadata
from thumblr.models import Image


def add_image(image_file, image_metadata):
    assert isinstance(image_metadata, ImageMetadata)

    image = Image()

    image.file_name = image_metadata.file_name
    image.file_type = image_metadata.file_type
    image.site_id = image_metadata.site_id

    image.object_content_type = image_metadata.content_type_id
    image.object_id = image_metadata.object_id

    image.storage = image_file

    image.save()