"""Use cases are the *only* entry points of thumblr lib, all parameters should be primitive python types, or DTO's (
data transfer objects)
"""

from django.db.transaction import atomic
from thumblr.dto import ImageMetadata
from thumblr.services.image_file_service import create_image_file, get_image_file_by_spec, get_image_file_url, \
    replace_uploaded_image
from thumblr.services.image_service import create_image


__all__ = ['add_image', 'get_image_file_url', 'update_image']


@atomic
def add_image(uploaded_file, image_metadata):
    assert isinstance(image_metadata, ImageMetadata)

    image = create_image(image_metadata)
    image_file = create_image_file(uploaded_file, image_metadata, image)

    return image, image_file


def get_image_url(image_metadata_spec, url_spec):
    assert isinstance(image_metadata_spec, ImageMetadata)

    image_file = get_image_file_by_spec(image_metadata_spec)

    return get_image_file_url(image_file, url_spec)


@atomic
def update_image(new_file, image_metadata):
    """Updates image specified by image_metadata spec with new_file.
       new_file - should be instance of django File
       image_metadata - ImageMetadata
    """
    assert isinstance(image_metadata, ImageMetadata)

    image_file = get_image_file_by_spec(image_metadata)
    replace_uploaded_image(image_file, new_file)

    return image_file

