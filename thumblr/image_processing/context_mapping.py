import cStringIO
import urllib
from PIL import Image
from thumblr import get_image_url, ImageMetadata, ImageUrlSpec


def get_pil_image_by_image_metadata(image_metadata):
    assert isinstance(image_metadata, ImageMetadata)

    image_url = get_image_url(image_metadata, ImageUrlSpec.S3_URL)

    stream = cStringIO.StringIO(
        urllib.urlopen(image_url).read()
    )
    img = Image.open(stream)

    return img