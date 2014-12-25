from thumblr import ImageMetadata
from thumblr.models import Image, ImageSize


def create_image(uploaded_file, image_metadata):
    assert isinstance(image_metadata, ImageMetadata)

    image = Image()

    image.original_file_name = image_metadata.original_file_name
    image.site_id = image_metadata.site_id
    image.content_type_id = image_metadata.content_type_id
    image.object_id = image_metadata.object_id

    image.image_in_storage = uploaded_file
    image.is_main = image_metadata.is_main or False

    original_size = ImageSize.objects.get(name=image_metadata.size_slug)
    image.size = original_size

    image.save()

    return image


def replace_uploaded_image(image_file, new_uploaded_image):
    image_file.image_in_storage = new_uploaded_image
    image_file.save()