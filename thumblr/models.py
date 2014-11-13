from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.conf import settings
from django_boto.s3.storage import S3Storage
from jsonfield import JSONField


s3 = S3Storage(
    bucket_name=settings.AWS_THUMBLR_BUCKET,
    key=settings.AWS_ACCESS_KEY_ID,
    secret=settings.AWS_SECRET_ACCESS_KEY,
)

class ImageOriginal(models.Model):
    file_name = models.CharField()
    image = models.ImageField(storage=s3)

class ImageHashed(models.Model):
    hash = models.CharField()
    image = models.ImageField(storage=s3)

class Image(models.Model):
    storage = models.ImageField(storage=s3, upload_to='thumblr_images')

    file_name = models.CharField(null=True, max_length=128)
    file_type = models.CharField(null=True, max_length=64)

    site = models.ForeignKey(Site, null=True)

    object_content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('object_content_type', 'object_id')

    meta_data = JSONField(null=True)