# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from .forms import NotificationForm


@login_required
def IndexView(request):
    return render(request, 'notification/index.html')


@require_http_methods(["GET", "POST"])
def CreateView(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            print 'valid'
            form.save()
            return render(request, 'notification/create.html', {'form': form, 'success': True})
        else:
            print form.errors
            print 'invalid'
            return render(request, 'notification/create.html', {'form': form, 'success': True})
    print timezone.get_current_timezone()
    form = NotificationForm
    return render(request, 'notification/create.html', {'form': form})
