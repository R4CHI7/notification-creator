from django.conf.urls import url

from notification.views import IndexView, CreateView

urlpatterns = [
    url(r'^$',       IndexView, name='index'),
    url(r'^create/', CreateView, name='create')
]
