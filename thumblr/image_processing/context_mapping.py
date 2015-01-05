import cStringIO
import urllib
from PIL import Image
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from thumblr import get_image_url, ImageMetadata, ImageUrlSpec


def get_pil_image_by_image_metadata(image_metadata):
    assert isinstance(image_metadata, ImageMetadata)

    image_url = get_image_url(image_metadata, ImageUrlSpec.S3_URL)

    stream = cStringIO.StringIO(
        urllib.urlopen(image_url).read()
    )
    img = Image.open(stream)

    return img


def get_django_file_from_pil_image(pil_image, format='JPEG'):
    assert isinstance(pil_image, Image.Image)

    stream = cStringIO.StringIO()
    pil_image.save(stream, format=format)

    stream.seek(0)

    return ContentFile(stream.read())