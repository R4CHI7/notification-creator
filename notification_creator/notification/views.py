# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .forms import NotificationForm
from .tasks import notify
from .common import getNotificationCountByStatus


@login_required
def IndexView(request):
    """
    Renders the home page with notification stats.
    """
    try:
        notifications_sent = getNotificationCountByStatus(2)
        notifications_scheduled = getNotificationCountByStatus(1)
        notifications_failed = getNotificationCountByStatus(3)
        template_data = {
            'notifications_sent': notifications_sent,
            'notifications_scheduled': notifications_scheduled,
            'notifications_failed': notifications_failed
            }
        return render(request, 'notification/index.html', template_data)
    except Exception as e:
        raise e


@login_required
@require_http_methods(["GET", "POST"])
def CreateView(request):
    """
    Renders the new notification form and accepts the form submission.
    If the data is valid, it schedules a notification task for celery.
    """
    if request.method == 'POST':
        try:
            form = NotificationForm(request.POST)
            if form.is_valid():
                # Save the notification and retrieve the saved instance.
                notification = form.save()

                # Schedule a new notification at `send_at`
                notify.apply_async((notification.id,), eta=notification.send_at)

                # Redirect user to homepage.
                return redirect('index')
            else:
                # Render the form with errors.
                return render(request, 'notification/create.html', {'form': form})
        except Exception as e:
            raise e

    # For GET requests, show the form.
    form = NotificationForm
    return render(request, 'notification/create.html', {'form': form})
