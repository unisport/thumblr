from datetime import datetime
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


class Image(models.Model):
    class Meta:
        db_table = "images"

    site = models.ForeignKey(Site, null=False, default=1)
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    original_file_name = models.CharField(max_length=256)


class ImageSize(models.Model):
    class Meta:
        db_table = "sizes"

    name = models.CharField(max_length=30)
    max_width = models.IntegerField()
    max_height = models.IntegerField()

    def __str__(self):
        return self.name


class ImageFile(models.Model):
    class Meta:
        db_table = "image_files"

    @staticmethod
    def upload_to():
        return 'images/{}'.format(datetime.strftime(datetime.today(), "%d%m%Y"),)

    image = models.ForeignKey(Image)
    image_in_storage = models.ImageField(storage=s3, upload_to=upload_to)
    image_hash = models.CharField(max_length=256)
    size = models.ForeignKey(ImageSize)
    meta_data = JSONField(null=True)

    # Here we can store old hash or link to old ImageFile object. Second one is much better!
    old = models.CharField(max_length=256)

    def __str__(self):
        return "{} Hash: {}".format(self.original_file_name, self.image_hash)


