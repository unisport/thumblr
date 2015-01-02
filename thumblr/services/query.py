from thumblr.dto import ImageMetadata
from thumblr.exceptions import NoSuchImageException
from thumblr.models import Image


def get_images_by_spec(image_spec, one=False):
    assert isinstance(image_spec, ImageMetadata)

    if not image_spec.image_file_id is None:
        r = get_image_by_id(image_spec.image_file_id)
        return r if one else [r]

    if not image_spec.image_hash is None:
        r = get_image_by_hash(image_spec.image_hash)
        return r if one else [r]

    q = Image.get_q(image_spec)

    images = Image.objects.filter(q)

    if one:
        image = images.first()

        if image is None:
            raise NoSuchImageException()

        return image

    return images


def get_image_by_id(image_file_id):
    try:
        return Image.objects.get(pk=image_file_id)
    except Image.DoesNotExist:
        raise NoSuchImageException()


def get_image_by_hash(image_hash):
    try:
        return Image.objects.get(image_hash=image_hash)
    except Image.DoesNotExist:
        raise NoSuchImageException()


def get_image_metadata(image):
    assert isinstance(image, Image)

    return ImageMetadata(
        image_file_id=image.id,
        image_hash=image.image_hash,

        file_name=image.original_file_name,
        site_id=image.site_id,
        size_slug=image.size.name,
        content_type_id=image.content_type_id,
        object_id=image.object_id,

        is_main=image.is_main,
    )