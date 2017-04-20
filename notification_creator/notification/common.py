from .models import Notification


def getNotificationCountByStatus(status):
    """
    Get number of notifications according to value of status.
    """
    try:
        count = Notification.objects.filter(status=status).count()
        return count
    except Exception as e:
        raise e
