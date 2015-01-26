from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.conf import settings
from django.db.models import Q
from django_boto.s3.storage import S3Storage
from jsonfield import JSONField
import ntpath
from thumblr.dto import ImageMetadata


s3 = S3Storage(
    bucket_name=settings.AWS_THUMBLR_BUCKET,
    key=settings.AWS_ACCESS_KEY_ID,
    secret=settings.AWS_SECRET_ACCESS_KEY,
)


class ImageSize(models.Model):

    ORIGINAL = 'original'
    SQUARED = 'squared'

    name = models.CharField(max_length=30, primary_key=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, related_name="image_sizes")

    def __unicode__(self):
        return '{name} - {model}'.format(name=self.name,
                                         model=self.content_type.name)


def upload_to(inst, filename):
    assert isinstance(inst, Image)

    # object id used to enalbe uploading of file of same names
    return u'{content_type}/{object_id}/{filename}'.format(
        content_type=inst.content_type.name.replace(u" ", u"_"),
        object_id=inst.object_id,
        filename=ntpath.basename(filename)
    )


def upload_to_hashed(inst, filename):
    assert isinstance(inst, Image)

    # object id used to enalbe uploading of file of same names
    return u'{content_type}/{object_id}/{filename}'.format(
        content_type=inst.content_type.name.replace(u" ", u"_"),
        object_id=inst.object_id,
        filename=inst.image_hash,
    )


class Image(models.Model):

    # site is optional here. Pictures should be available across all sites.
    # I left it here in case the product is dedicated to one specific country's site
    site = models.ForeignKey(Site, null=True)

    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    file_name = models.CharField(max_length=256, default='')

    image_in_storage = models.ImageField(storage=s3, upload_to=upload_to)
    image_hash_in_storage = models.ImageField(storage=s3, upload_to=upload_to_hashed)
    image_hash = models.CharField(max_length=256)
    size = models.ForeignKey(ImageSize)
    meta_data = JSONField(null=True, blank=True)

    is_main = models.BooleanField(default=False)
    order_number = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return u"%s::%s::%s::%s::%s::%s" % (
            self.id,
            self.file_name,
            self.site.name if self.site else u'',
            self.image_hash,
            self.id,
            self.size.name if self.size else u'',
        )

    @classmethod
    def get_q(cls, image_spec):
        assert isinstance(image_spec, ImageMetadata)

        q = Q()

        if not image_spec.image_file_id is None:
            q &= Q(pk=image_spec.image_file_id)

        if not image_spec.file_name is None:
            q &= Q(file_name=image_spec.file_name)

        if not image_spec.site_id is None:
            if image_spec.site_id == ImageMetadata.SITE_IS_NULL:
                q &= Q(site_id__isnull=True)
            else:
                q &= Q(site_id=image_spec.site_id)

        if not image_spec.content_type_id is None:
            q &= Q(content_type_id=image_spec.content_type_id)

        if not image_spec.object_id is None:
            q &= Q(object_id=image_spec.object_id)

        if not image_spec.image_hash is None:
            q &= Q(image_hash=image_spec.image_hash)

        if not image_spec.is_main is None:
            q &= Q(is_main=image_spec.is_main)

        if not image_spec.size_slug is None:
            q &= Q(size__name=image_spec.size_slug)

        return q
