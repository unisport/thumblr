from thumblr.dto import ImageMetadata
from thumblr.exceptions import NoSuchImageException
from thumblr.models import Image


def create_image(image_metadata):
    assert isinstance(image_metadata, ImageMetadata)

    image = Image()

    image.original_file_name = image_metadata.original_file_name
    image.site_id = image_metadata.site_id
    image.content_type_id = image_metadata.content_type_id
    image.object_id = image_metadata.object_id
    image.save()

    return image


def get_images_by_spec(image_spec, one=False):
    assert isinstance(image_spec, ImageMetadata)

    images = Image.objects.filter(
        Image.get_q(image_spec)
    )

    if one:
        image = images.first()

        if image is None:
            raise NoSuchImageException()

        return image

    return images
