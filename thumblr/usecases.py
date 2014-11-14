from boto.sdb.db import model
from thumblr.dto import ImageMetadata
from thumblr.models import Image, ImageFile, ImageSize
from thumblr.utils.hash import file_hash


def add_image(image_file, image_metadata):
    assert isinstance(image_metadata, ImageMetadata)

    image = Image()

    image.original_file_name = image_metadata.original_file_name
    image.site = image_metadata.site
    image.content_type = image_metadata.content_type
    image.object_id = image_metadata.object_id
    image.save()

    image_file_inst = ImageFile()
    image_file_inst.image = image
    image_file_inst.image_in_storage = image_file
    image_file_inst.image_hash = file_hash(image_file.file)

    try:
        original_size = ImageSize.objects.get(name='original')
    except ImageSize.DoesNotExist:
        original_size = ImageSize(name='original')

    image_file_inst.size = original_size





