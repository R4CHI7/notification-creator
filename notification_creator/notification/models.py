# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinLengthValidator


class Notification(models.Model):
    STATUS_CHOICES = (
        (1, 'scheduled'),
        (2, 'success'),
        (3, 'failure'),
    )
    header = models.CharField(max_length=150, validators=[MinLengthValidator(20)])
    content = models.CharField(max_length=300, validators=[MinLengthValidator(20)])
    image_url = models.URLField()
    send_at = models.DateTimeField(verbose_name='Send at')
    user_query = models.TextField(verbose_name='User query')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notification'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
