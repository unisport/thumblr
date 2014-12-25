from thumblr.dto import ImageUrlSpec
from thumblr.exceptions import IncorrectUrlSpecException
from thumblr.models import Image
from thumblr.utils.cdn import get_cdn_domain


def get_image_instance_url(image, url_spec):
    assert isinstance(image, Image)

    if url_spec == ImageUrlSpec.S3_URL:
        return image.image_hash_in_storage.url
    elif url_spec == ImageUrlSpec.CDN_URL:
        return u"{domain}/{path}".format(
            domain=get_cdn_domain(image.image_hash),
            path=image.image_hash_in_storage.name
        )
    elif url_spec == ImageUrlSpec.PATH_ONLY_URL:
        return image.image_hash_in_storage.name
    else:
        raise IncorrectUrlSpecException()