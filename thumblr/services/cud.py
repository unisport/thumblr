from thumblr.dto import ImageMetadata
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


def replace_uploaded_image(image, new_uploaded_image):
    assert isinstance(image, Image)

    image.image_in_storage = new_uploaded_image
    image.save()


def update_image_metadata(image, updated_spec):
    assert isinstance(image, Image)
    assert isinstance(updated_spec, ImageMetadata)

    if not updated_spec.original_file_name is None:
        image.original_file_name = updated_spec.original_file_name

    if not updated_spec.site_id is None:
        image.site_id = updated_spec.site_id

    if not updated_spec.content_type_id is None:
        image.content_type_id = updated_spec.content_type_id

    if not updated_spec.object_id is None:
        image.object_id = updated_spec.object_id

    if not updated_spec.is_main is None:
        image.is_main = updated_spec.is_main

    if not updated_spec.size_slug is None:
        image_size = ImageSize.objects.get(name=updated_spec.size_slug)
        image.size = image_size

    image.save()
