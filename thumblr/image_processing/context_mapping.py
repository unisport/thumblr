import cStringIO
from PIL import Image
from django.core.files.base import ContentFile
from thumblr import ImageMetadata, ImageUrlSpec
from thumblr.usecases import get_image_data


def get_pil_image_by_image_metadata(image_metadata):
    assert isinstance(image_metadata, ImageMetadata)

    stream = get_image_data(image_metadata, ImageUrlSpec.S3_URL)
    img = Image.open(stream)

    return img


def get_django_file_from_pil_image(pil_image, format='JPEG'):
    assert isinstance(pil_image, Image.Image)

    stream = cStringIO.StringIO()
    pil_image.save(stream, format=format)

    stream.seek(0)

    return ContentFile(stream.read())