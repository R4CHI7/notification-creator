# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
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
            form.save()
            return redirect('index')
        else:
            return render(request, 'notification/create.html', {'form': form})
    form = NotificationForm
    return render(request, 'notification/create.html', {'form': form})
