from thumblr.dto import ImageMetadata, ImageUrlSpec
from thumblr.exceptions import NoSuchImageException, IncorrectUrlSpecException
from thumblr.models import ImageFile, Image, ImageSize
from thumblr.services.image_service import get_images_by_spec
from thumblr.utils.cdn import get_cdn_domain


def create_image_file(uploaded_file, image_metadata, image_inst):
    assert isinstance(image_metadata, ImageMetadata)
    assert isinstance(image_inst, Image)

    image_file = ImageFile()
    image_file.image = image_inst
    image_file.image_in_storage = uploaded_file
    image_file.is_main = image_metadata.is_main or False

    original_size = ImageSize.objects.get(name=image_metadata.size_slug)
    image_file.size = original_size

    image_file.save()

    return image_file


def replace_uploaded_image(image_file, new_uploaded_image):
    image_file.image_in_storage = new_uploaded_image
    image_file.save()


def get_image_file_by_id(image_file_id):
    try:
        return ImageFile.objects.get(pk=image_file_id)
    except ImageFile.DoesNotExist:
        raise NoSuchImageException()


def get_image_file_by_hash(image_hash):
    try:
        return ImageFile.objects.get(image_hash=image_hash)
    except ImageFile.DoesNotExist:
        raise NoSuchImageException()


def get_image_files_by_spec(image_spec, one=False):
    assert isinstance(image_spec, ImageMetadata)

    if not image_spec.image_file_id is None:
        return get_image_file_by_id(image_spec.image_file_id)

    if not image_spec.image_hash is None:
        return get_image_file_by_hash(image_spec.image_hash)

    res = []

    for image in get_images_by_spec(image_spec):
        res.extend(
            image.imagefile_set.filter(
                ImageFile.get_q(image_spec)
            )
        )

    if not res and one:
        raise NoSuchImageException()

    if one:
        return res[0]
    else:
        return res


def get_image_file_url(image_file, url_spec):
    assert isinstance(image_file, ImageFile)

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


def get_image_file_metadata(image_file):
    assert isinstance(image_file, ImageFile)

    return ImageMetadata(
        image_file_id=image_file.id,
        image_hash=image_file.image_hash,

        file_name=image_file.image.original_file_name,
        site_id=image_file.image.site_id,
        size_slug=image_file.size.name,
        content_type_id=image_file.image.content_type_id,
        object_id=image_file.image.object_id,
    )