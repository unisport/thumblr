from thumblr.dto import ImageMetadata, ImageUrlSpec
from thumblr.exceptions import NoSuchImageException, IncorrectUrlSpecException
from thumblr.models import ImageFile, Image, ImageSize
from thumblr.services.image_service import get_image_by_spec
from thumblr.utils.cdn import get_cdn_domain


def create_image_file(uploaded_file, image_metadata, image_inst):
    assert isinstance(image_metadata, ImageMetadata)
    assert isinstance(image_inst, Image)

    image_file = ImageFile()
    image_file.image = image_inst
    image_file.image_in_storage = uploaded_file

    original_size = ImageSize.objects.get(name=image_metadata.size_slug)
    image_file.size = original_size

    image_file.save()

    return image_file


def get_image_file_by_spec(image_spec):
    assert isinstance(image_spec, ImageMetadata)

    image = get_image_by_spec(image_spec)

    image_file = image.imagefile_set.filter(
        ImageFile.get_q(image_spec)
    ).first()

    if image_file is None:
        raise NoSuchImageException()

    return image_file


def get_image_file_url(image_file, url_spec):
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
