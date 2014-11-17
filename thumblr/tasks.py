
from django.conf import settings

from celery import Celery, Task
from raven import Client

import usecases


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

usecases.add_image = celery.task(usecases.add_image)