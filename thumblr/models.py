from datetime import datetime
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


class Image(models.Model):

    site = models.ForeignKey(Site, null=False, default=1)
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    original_file_name = models.CharField(max_length=256)

    def __str__(self):
        return "{file_name} [{site}]".format(
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
    return 'images/{date}/{filename}'.format(date=datetime.today().strftime("%d-%m-%Y"),
                                             filename=ntpath.basename(filename))


class ImageFile(models.Model):

    image = models.ForeignKey(Image)
    image_in_storage = models.ImageField(storage=s3, upload_to=upload_to)
    image_hash_in_storage = models.ImageField(storage=s3, upload_to=upload_to)
    image_hash = models.CharField(max_length=256)
    size = models.OneToOneField(ImageSize)
    meta_data = JSONField(null=True)

    def __str__(self):
        return "{file_name} Hash: {hash}".format(
            file_name=self.original_file_name,
            hash=self.image_hash
        )

    @classmethod
    def get_q(cls, image_spec):
        q = Q()
        if not image_spec.size_slug is None:
            q &= Q(size__name=image_spec.size_slug)

        return q

