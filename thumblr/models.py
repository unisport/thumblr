from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.files import File
from django.db import models
from django.conf import settings
from django.db.models import Q
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django_boto.s3.storage import S3Storage
from jsonfield import JSONField
import ntpath
import os
from thumblr.dto import ImageMetadata
from thumblr.utils.hash import file_hash


s3 = S3Storage(
    bucket_name=settings.AWS_THUMBLR_BUCKET,
    key=settings.AWS_ACCESS_KEY_ID,
    secret=settings.AWS_SECRET_ACCESS_KEY,
)


class Image(models.Model):

    # site is optional here. Pictures should be available across all sites.
    # I left it here in case the product is dedicated to one specific country's site
    site = models.ForeignKey(Site, null=True)
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    original_file_name = models.CharField(max_length=256)

    def __str__(self):
        return "{image_id}::{file_name}::{site}".format(
            image_id=self.id,
            file_name=self.original_file_name,
            site=self.site.name,
        )

    @classmethod
    def get_q(cls, image_spec):
        assert isinstance(image_spec, ImageMetadata)

        q = Q()

        if not image_spec.original_file_name is None:
            q &= Q(original_file_name=image_spec.original_file_name)

        if not image_spec.site_id is None:
            q &= Q(site_id=image_spec.site_id)

        if not image_spec.content_type_id is None:
            q &= Q(content_type_id=image_spec.content_type_id)

        if not image_spec.object_id is None:
            q &= Q(object_id=image_spec.object_id)

        return q


class ImageSize(models.Model):

    ORIGINAL = 'original'

    name = models.CharField(max_length=30, primary_key=True)
    max_width = models.IntegerField(null=True, blank=True)
    max_height = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


def upload_to(inst, filename):
    assert isinstance(inst, ImageFile)

    # object id used to enalbe uploading of file of same names
    return u'{content_type}/{object_id}/{filename}'.format(
        content_type=inst.image.content_type.name.replace(u" ", u"_"),
        object_id=inst.image.object_id,
        filename=ntpath.basename(filename)
    )


class ImageFile(models.Model):

    image = models.ForeignKey(Image)
    image_in_storage = models.ImageField(storage=s3, upload_to=upload_to)
    image_hash_in_storage = models.ImageField(storage=s3, upload_to=upload_to)
    image_hash = models.CharField(max_length=256)
    size = models.ForeignKey(ImageSize)
    meta_data = JSONField(null=True, blank=True)

    def __str__(self):
        return "{image_file_id}::{file_name}::{size}::{hash}".format(
            file_name=self.image.original_file_name,
            hash=self.image_hash,
            image_file_id=self.id,
            size=self.size.name,
        )

    @classmethod
    def get_q(cls, image_spec):
        assert isinstance(image_spec, ImageMetadata)

        q = Q()

        if not image_spec.image_file_id is None:
            q &= Q(pk=image_spec.image_file_id)

        if not image_spec.image_hash is None:
            q &= Q(image_hash=image_spec.image_hash)

        if not image_spec.size_slug is None:
            q &= Q(size__name=image_spec.size_slug)

        return q


@receiver(pre_save, sender=ImageFile)
def fill_hashed_image_fields(sender, instance, *args, **kwargs):
    assert isinstance(instance, ImageFile)

    uploaded_image = instance.image_in_storage

    hashed_file_name = file_hash(uploaded_image) + os.path.splitext(uploaded_image.name)[-1]

    file_by_hash = File(
        uploaded_image,
        hashed_file_name
    )

    instance.image_hash_in_storage = file_by_hash

    # File with hashed name and original file extension
    instance.image_hash = hashed_file_name
