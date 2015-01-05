from django.core.cache import get_cache, cache, InvalidCacheBackendError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from thumblr.models import Image
from thumblr.dto import ImageMetadata, ImageUrlSpec
from thumblr.services.query import get_image_by_id


try:
    thumblr_cache = get_cache('thumblr')
except InvalidCacheBackendError:
    thumblr_cache = cache

# pinging on cache
thumblr_cache.get("FOO")


def _get_key(f, *args):
    return "{func_name}:{arg}".format(
        func_name=f.func_name,
        arg="_".join(map(str, args)),
    )


def cached(f):
    """Simple cache for functions, cached function **must** get only **positional** arguments, which have unique
    __str__ return value"""

    def cached_f(*args):
        key = _get_key(f, *args)

        val = thumblr_cache.get(key)

        if val:
            return val

        val = f(*args)
        thumblr_cache.set(key, val)

        return val

    cached_f.func_name = f.func_name

    return cached_f


def drop_cache_for(f, *args):
    key = _get_key(f, *args)

    thumblr_cache.delete(key)


@receiver(pre_save, sender=Image)
def __drop_url_cache(sender, instance, *args, **kwargs):
    assert isinstance(instance, Image)

    from thumblr.usecases import get_image_url

    if instance.id:
        old_inst = get_image_by_id(instance.pk)
        drop_cache_for(
            get_image_url,
            ImageMetadata(
                image_file_id=old_inst.id,
                file_name=old_inst.original_file_name,
                size_slug=old_inst.size.name,
                content_type_id=old_inst.content_type_id,
                object_id=old_inst.object_id,
            ),
            ImageUrlSpec.CDN_URL,
        )