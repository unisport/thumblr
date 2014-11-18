from django.core.files import File
import os
from django.db.transaction import atomic
from thumblr.dto import ImageMetadata, ImageUrlSpec
from thumblr.exceptions import NoSuchImageException, IncorrectUrlSpecException
from thumblr.models import Image, ImageFile, ImageSize
from thumblr.utils.cdn import get_cdn_domain
from thumblr.utils.hash import file_hash


@atomic
def add_image(uploaded_file, image_metadata):
    assert isinstance(image_metadata, ImageMetadata)

    image = Image()

    image.original_file_name = image_metadata.original_file_name
    image.site_id = image_metadata.site_id
    image.content_type_id = image_metadata.content_type_id
    image.object_id = image_metadata.object_id
    image.save()

    image_file = ImageFile()
    image_file.image = image
    image_file.image_in_storage = uploaded_file

    hashed_file_name = file_hash(uploaded_file) + os.path.splitext(uploaded_file.name)[-1]

    file_by_hash = File(
        uploaded_file,
        hashed_file_name
    )

    image_file.image_hash_in_storage = file_by_hash

    # File with hashed name and original file extension
    image_file.image_hash = hashed_file_name

    original_size = ImageSize.objects.get(name=image_metadata.size_slug)

    image_file.size = original_size

    image_file.save()


def get_image_url(image_metadata_spec, url_spec=False):
    assert isinstance(image_metadata_spec, ImageMetadata)

    image = Image.objects.filter(
        Image.get_q(image_metadata_spec)
    ).first()

    if image is None:
        raise NoSuchImageException()

    image_file = image.imagefile_set.filter(
        ImageFile.get_q(image_metadata_spec)
    ).first()

    if image_file is None:
        raise NoSuchImageException()

    if url_spec == ImageUrlSpec.S3_URL:
        return image_file.image_hash_in_storage.url
    elif url_spec == ImageUrlSpec.CDN_URL:
        return u"{domain}/{path}".format(
            domain=get_cdn_domain(image_file.image_hash),
            path=image_file.image_hash_in_storage.name
        )
    elif url_spec == ImageUrlSpec.PATH_ONLY_URL:
        return image_file.image_hash_in_storage.name
    else:
        raise IncorrectUrlSpecException()




