from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger

from .models import Notification
from .utils import sendNotification


logger = get_task_logger(__name__)


@shared_task
def notify(notification_id):
    """
    The main Celery task.

    Receives an ID for a newly scheduled notification, sends the notification and updates
    status in the database.
    """
    try:
        notification = Notification.objects.get(id=notification_id)
        notification_payload = {
            'header': notification.header,
            'content': notification.content,
            'image_url': notification.image_url
        }
        return_value = False
        result = sendNotification(notification.user_query, notification_payload)
        if result:
            notification.status = 2
            return_value = True
        else:
            notification.status = 3
    except Exception as e:
        logger.error('Error occurred while running task: ' + str(e))
        notification.status = 3
    finally:
        notification.save()
        return return_value
