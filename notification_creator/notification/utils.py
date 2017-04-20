import random


def sendNotification(user_ids, notification_payload):
    """
    Simulated method which returns True/False with 50/50 probability.
    """
    return random.randrange(10) < 5
