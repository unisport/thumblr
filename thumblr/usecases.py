"""Use cases are the *only* entry points of thumblr lib, all parameters should be primitive python types, or DTO's (
data transfer objects)
"""

from django.db.transaction import atomic
from thumblr.caching import cached
from thumblr.dto import ImageMetadata
from thumblr.services.cud import create_image, replace_uploaded_image, update_image_metadata
from thumblr.services.query import get_image_metadata, get_images_by_spec
from thumblr.services.url import get_image_instance_url


__all__ = ['add_image', 'get_image_url', 'update_image', 'update_images_metadata', 'delete_images',
           'get_all_images', 'get_images_of_sizes']


@atomic
def add_image(uploaded_file, image_metadata):
    assert isinstance(image_metadata, ImageMetadata)

    image = create_image(uploaded_file, image_metadata)

    return get_image_metadata(image)


@cached
def get_image_url(image_metadata, url_spec):
    """
    `image_file_id`, `file_name` and `size_slug` in image_metadata_spec are required for correct url caching
    """
    assert isinstance(image_metadata, ImageMetadata)

    image_file = get_images_by_spec(image_metadata, one=True)

    return get_image_instance_url(image_file, url_spec)


@atomic
def update_image(new_file, image_metadata):
    """Updates image specified by image_metadata spec with new_file.
       new_file - should be instance of django File
       image_metadata - ImageMetadata
    """
    assert isinstance(image_metadata, ImageMetadata)

    image_file = get_images_by_spec(image_metadata, one=True)
    replace_uploaded_image(image_file, new_file)

    return get_image_metadata(image_file)


@atomic
def update_images_metadata(image_spec, updated_spec):
    assert isinstance(image_spec, ImageMetadata)
    assert isinstance(updated_spec, ImageMetadata)

    images = get_images_by_spec(image_spec)

    for image in images:
        update_image_metadata(image, updated_spec)


@atomic
def delete_images(image_metadata, excepted=None):
    """
    Removes all images that meet criteria of `image_metadata`
    """
    assert isinstance(image_metadata, ImageMetadata)
    assert isinstance(excepted, (type(None), ImageMetadata, list))

    image_files = get_images_by_spec(image_metadata)

    if excepted is None:
        except_file_ids = []
    elif isinstance(excepted, ImageMetadata):
        except_file_ids = [item.id for item in get_images_by_spec(excepted)]
    else:
        except_file_ids = []
        for d in excepted:
            except_file_ids.extend([item.id for item in get_images_by_spec(d)])

    for image_file in image_files:
        if not image_file.id in except_file_ids:
            image_file.delete()


def get_all_images(image_metadata, ordered=False):
    assert isinstance(image_metadata, ImageMetadata)

    images = get_images_by_spec(image_metadata, ordered=ordered)
    return map(get_image_metadata, images)


def get_images_of_sizes(image_metadata):
    """
    Retrieves all images by image_metadata as dict like:
    {
      image_size_slug: ImageMetadata,
      ...
    }
    """
    assert isinstance(image_metadata, ImageMetadata)

    res = {}
    for image in get_all_images(image_metadata):
        assert isinstance(image, ImageMetadata)
        res[image.size_slug] = image

    return res
