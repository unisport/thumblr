import os
from django.db.transaction import atomic
from thumblr.dto import ImageMetadata
from thumblr.models import Image, ImageFile, ImageSize
from thumblr.utils.hash import file_hash


@atomic
def add_image(uploaded_file, image_metadata):
    assert isinstance(image_metadata, ImageMetadata)

    image = Image()

    image.original_file_name = image_metadata.original_file_name
    image.site_id = image_metadata.site_id
    image.content_type_id = image_metadata.content_type
    image.object_id = image_metadata.object_id
    image.save()

    image_file = ImageFile()
    image_file.image = image
    image_file.image_in_storage = uploaded_file

    uploaded_file_hash = uploaded_file
    hash_by_content = file_hash(uploaded_file)
    uploaded_file_hash.name = hash_by_content + os.path.splitext(uploaded_file.name)[-1]

    image_file.image_hash_in_storage = uploaded_file_hash
    # File with hashed name and original file extension
    image_file.image_hash = hash_by_content

    original_size = ImageSize.objects.get(name='original')

    image_file.size = original_size

    image_file.save()





