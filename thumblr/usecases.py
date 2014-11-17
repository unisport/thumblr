from django.db.transaction import atomic
from django.conf import settings

from celery import Celery, Task
from raven import Client

from thumblr.dto import ImageMetadata, ImageUrlSpec
from thumblr.exceptions import NoSuchImageException, IncorrectUrlSpecException
from thumblr.models import Image, ImageFile, ImageSize
from thumblr.utils.cdn import get_cdn_domain
from thumblr.utils.hash import file_hash

client = Client(settings.SENTRY_DSN)
celery = Celery('tasks')

celery.conf.update(
    AWS_ACCESS_KEY_ID=settings.AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY=settings.AWS_SECRET_ACCESS_KEY,
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    BROKER_URL="sqs://%s:%s@" % (settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY),
    CELERY_RESULT_BACKEND="redis",
    CELERY_TIMEZONE='Europe/Copenhagen',
    BROKER_TRANSPORT_OPTIONS={'region': 'eu-west-1',
                              'polling_interval': 0.3,
                              'visibility_timeout': 3600,
                              'queue_name_prefix': 'catalog_products_'},
)


class ImagesCallbackTask(Task):
    """
    Generic subclass for Product Image Processing tasks
    so in case of of failure, a notification is sent to Sentry.
    """

    # def on_success(self, retval, task_id, args, kwargs):
    #     pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # client.captureMessage('Task "%s" has failed miserably.' % task_id)
        client.capture('raven.events.Message', message='Task "%s" has failed miserably.' % task_id,
                        data={},
                        extra={'exc': exc,
                               'Task ID': task_id,
                               'Args': args,
                               'Kwargs': kwargs,
                               'einfo': einfo
                              }
                      )


@atomic
@celery.task(base=ImagesCallbackTask, name='add_image')
def add_image(uploaded_file, image_metadata):
    assert isinstance(image_metadata, ImageMetadata)

    image = Image()

    image.original_file_name = image_metadata.original_file_name
    image.site_id = image_metadata.site_id
    image.content_type_id = image_metadata.content_type_id
    image.object_id = image_metadata.object_id
    image.save()

    image_file = ImageFile()
    image_file.image = image
    image_file.image_in_storage = uploaded_file
    image_file.image_hash = file_hash(uploaded_file)

    original_size = ImageSize.objects.get(name='original')

    image_file.size = original_size

    image_file.save()


def get_image_url(image_metadata_spec, url_spec=False):
    assert isinstance(image_metadata_spec, ImageMetadata)

    image = Image.objects.filter(
        Image.get_q(image_metadata_spec)
    ).first()

    image_file = image.imagefile_set.filter(
        ImageFile.get_q(image_metadata_spec)
    ).first()

    if image_file is None:
        raise NoSuchImageException()

    if url_spec == ImageUrlSpec.S3_URL:
        return image_file.image_hash_in_storage.url
    elif url_spec == ImageUrlSpec.CDN_URL:
        return u"{domain}{path}".format(
            domain=get_cdn_domain(image_file.image_hash),
            path=image_file.image_hash_in_storage.name
        )
    elif url_spec == ImageUrlSpec.PATH_ONLY_URL:
        return image_file.image_hash_in_storage.name
    else:
        raise IncorrectUrlSpecException()




