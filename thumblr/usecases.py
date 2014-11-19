from django.db.transaction import atomic
from thumblr.dto import ImageMetadata
from thumblr.services.image_file_service import create_image_file, get_image_file_by_spec, get_image_file_url
from thumblr.services.image_service import create_image


@atomic
def add_image(uploaded_file, image_metadata):
    assert isinstance(image_metadata, ImageMetadata)

    image = create_image(image_metadata)
    image_file = create_image_file(uploaded_file, image_metadata, image)


def get_image_url(image_metadata_spec, url_spec):
    assert isinstance(image_metadata_spec, ImageMetadata)

    image_file = get_image_file_by_spec(image_metadata_spec)

    return get_image_file_url(image_file, url_spec)



