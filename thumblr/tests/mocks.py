from contextlib import contextmanager
from copy import deepcopy
from django.contrib.contenttypes.models import ContentType
from thumblr import ImageMetadata
from thumblr.exceptions import NoSuchImageException

__mocked = False


def mock_for_tests(f):
    def _f(*args, **kwargs):
        if is_mocked():
            if f.__name__ in __usecases_func_map_to_mocks:
                return __usecases_func_map_to_mocks[f.__name__](*args, **kwargs)
            else:
                return mock_func(*args, **kwargs)
        else:
            return f(*args, **kwargs)

    return _f


def mock_func(img, *args, **kwargs):
    return img


def thumblr_pil_mock_deco(f):
    def _f(*args, **kwargs):
        with thumblr_pil_mock():
            return f(*args, **kwargs)

    return _f


@contextmanager
def thumblr_pil_mock():
    set_mocked(True)
    yield
    set_mocked(False)


def set_mocked(flag):
    global __mocked
    __mocked = flag


def is_mocked():
    return __mocked


#####################
## usecases mocks  ##
#####################

__images_storage = []
__ID = 0


def reset_thumblr_usecases_mock():
    global __images_storage
    __images_storage = []


def _get_next_id():
    global __ID
    __ID += 1
    return __ID


def _equal(dto_val, filtr_val):
    if filtr_val == ImageMetadata.SITE_IS_NULL:
        return dto_val is None

    if filtr_val is None:
        return True

    return filtr_val == dto_val


def _find_image(image_metadata):
    assert isinstance(image_metadata, ImageMetadata)

    for dto, content in __images_storage:
        assert isinstance(dto, ImageMetadata)

        if _equal(dto.size_slug, image_metadata.size_slug) and \
           _equal(dto.content_type_id, image_metadata.content_type_id) and \
           _equal(dto.object_id, image_metadata.object_id) and \
           _equal(dto.file_name, image_metadata.file_name) and \
           _equal(dto.image_file_id, image_metadata.image_file_id) and \
           _equal(dto.site_id, image_metadata.site_id):
            yield dto, content


def _get_index_by_id(im_id):
    for i, x in enumerate(__images_storage):
        if x[0].image_file_id == im_id:
           return i
    raise NoSuchImageException


def mock__add_image(uploaded_file, image_metadata):
    assert isinstance(image_metadata, ImageMetadata)

    dto = deepcopy(image_metadata)
    assert isinstance(dto, ImageMetadata)
    id = _get_next_id()
    dto.image_file_id = id
    dto.image_hash = str(id)

    __images_storage.append(
        (dto, uploaded_file)
    )

    return dto


def mock__get_image_url(image_metadata, url_spec):
    """
    `image_file_id`, `file_name` and `size_slug` in image_metadata_spec are required for correct url caching
    """
    assert isinstance(image_metadata, ImageMetadata)

    try:
        dto, _ = next(_find_image(image_metadata))
    except StopIteration:
        raise NoSuchImageException

    return u"https://testing.awazonaws.com/{content_type}/{object_id}/{image_name}".format(
        content_type=ContentType.objects.get(pk=dto.content_type_id),
        object_id=dto.object_id,
        image_name=dto.file_name,
    )


def mock__update_image(new_file, image_metadata):
    """Updates image specified by image_metadata spec with new_file.
       new_file - should be instance of django File
       image_metadata - ImageMetadata
    """
    assert isinstance(image_metadata, ImageMetadata)

    try:
        dto, _ = next(_find_image(image_metadata))
    except StopIteration:
        raise NoSuchImageException

    __images_storage[dto.image_file_id] = (dto, new_file)

    return dto


def mock__update_images_metadata(image_spec, updated_spec):
    assert isinstance(image_spec, ImageMetadata)
    assert isinstance(updated_spec, ImageMetadata)

    for dto, content in _find_image(image_spec):
        __images_storage[_get_index_by_id(dto.image_file_id)] = (updated_spec, content)


def mock__delete_images(image_metadata, excepted=None):
    """
    Removes all images that meet criteria of `image_metadata`
    """
    assert isinstance(image_metadata, ImageMetadata)
    assert isinstance(excepted, (type(None), ImageMetadata, list))

    if excepted is None:
        excepted = []
    elif isinstance(excepted, ImageMetadata):
        excepted = [excepted]

    do_not_delete = []
    for x in excepted:
        do_not_delete.extend(map(lambda x: x[0], _find_image(x)))

    for dto, _ in reversed(list(_find_image(image_metadata))):
        assert isinstance(dto, ImageMetadata)
        delete = True
        for x in do_not_delete:
            assert isinstance(x, ImageMetadata)
            if dto.image_file_id == x.image_file_id:
                delete = False
                break

        if delete:
            del __images_storage[_get_index_by_id(dto.image_file_id)]


def mock__get_all_images(image_metadata, ordered=False):
    assert isinstance(image_metadata, ImageMetadata)
    res = []
    for dto, _ in _find_image(image_metadata):
        res.append(dto)

    if ordered:
        res = sorted(res, key=lambda item: item.order_number)

    return res


def mock__get_images_of_sizes(image_metadata):
    """
    Retrieves all images by image_metadata as dict like:
    {
      image_size_slug: ImageMetadata,
      ...
    }
    """
    assert isinstance(image_metadata, ImageMetadata)

    res = {}
    for dto, _ in _find_image(image_metadata):
        if not dto.size_slug in res:
            res[dto.size_slug] = dto

    return res


__usecases_func_map_to_mocks = {
    'add_image': mock__add_image,
    'get_image_url': mock__get_image_url,
    'update_image': mock__update_image,
    'update_images_metadata': mock__update_images_metadata,
    'delete_images': mock__delete_images,
    'get_all_images': mock__get_all_images,
    'get_images_of_sizes': mock__get_images_of_sizes,
}
