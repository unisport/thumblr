"""Use cases are the *only* entry points of thumblr lib, all parameters should be primitive python types, or DTO's (
data transfer objects)
"""
from django.db.models.signals import pre_save, post_save

from django.dispatch import receiver
from django.db.transaction import atomic
from thumblr.caching import cached, drop_cache_for
from thumblr.dto import ImageMetadata, ImageUrlSpec
from thumblr.models import ImageFile
from thumblr.services.image_file_service import create_image_file, get_image_file_by_spec, get_image_file_url, \
    replace_uploaded_image, get_image_file_by_id
from thumblr.services.image_service import create_image


__all__ = ['add_image', 'get_image_file_url', 'update_image']


@atomic
def add_image(uploaded_file, image_metadata):
    assert isinstance(image_metadata, ImageMetadata)

    image = create_image(image_metadata)
    image_file = create_image_file(uploaded_file, image_metadata, image)

    return image, image_file


@cached
def get_image_url(image_metadata_spec, url_spec):
    """
    `image_file_id`, `file_name` and `size_slug` in image_metadata_spec are required for correct url caching
    """
    assert isinstance(image_metadata_spec, ImageMetadata)

    image_file = get_image_file_by_spec(image_metadata_spec)

    return get_image_file_url(image_file, url_spec)


@atomic
def update_image(new_file, image_metadata):
    """Updates image specified by image_metadata spec with new_file.
       new_file - should be instance of django File
       image_metadata - ImageMetadata
    """
    assert isinstance(image_metadata, ImageMetadata)

    image_file = get_image_file_by_spec(image_metadata)
    replace_uploaded_image(image_file, new_file)

    return image_file


@receiver(pre_save, sender=ImageFile)
def __drop_url_cache(sender, instance, *args, **kwargs):
    assert isinstance(instance, ImageFile)

    if instance.id:
        old_inst = get_image_file_by_id(instance.pk)
        drop_cache_for(
            get_image_url,
            ImageMetadata(
                image_file_id=old_inst.id,
                file_name=old_inst.image.original_file_name,
                size_slug=old_inst.size.name,
            ),
            ImageUrlSpec.CDN_URL,
        )
