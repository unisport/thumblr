import urllib
from cStringIO import StringIO

from PIL.Image import Image
from django.conf import settings
from . import basic_operations
from thumblr.image_processing.basic_operations import ImagePos


BUBBLE_PATH = "{media_url}images/sparbobler/".format(media_url=settings.MEDIA_URL)
WATERMARK_PATH = "{media_url}images/watermark/".format(media_url=settings.MEDIA_URL)


def get_bubble_url_for(percentage):
    return "{bubble_path}{percentage}.png".format(
        bubble_path=BUBBLE_PATH,
        percentage=int(percentage),
    )


def get_watermark_url_for(site_id):
    return "{watermark_path}{site_id}_product.png".format(
        watermark_path=WATERMARK_PATH,
        site_id=site_id,
    )


def get_bubble_image_for(percentage):
    return Image.open(
        StringIO(
            urllib.urlopen(
                get_bubble_url_for(percentage)
            ).read()
        )
    )


def get_watermark_image_for(site_id):
    return Image.open(
        StringIO(
            urllib.urlopen(
                get_watermark_url_for(site_id)
            ).read()
        )
    )


def put_bubble_on_image(image, percentage):
    bubble_image = get_bubble_image_for(percentage)
    result_image = basic_operations.overlay(
        image,
        bubble_image,
        ImagePos(x=5, y=5)
    )

    return result_image


def put_watermark_on_image(image, site_id):
    watermark_image = get_watermark_image_for(site_id)
    result_image = basic_operations.overlay(
        image,
        watermark_image,
        ImagePos(
            x=image.size[0] - watermark_image.size[0] - 5,
            y=image.size[1] - watermark_image.size[1] - 5,
        )
    )

    return result_image
