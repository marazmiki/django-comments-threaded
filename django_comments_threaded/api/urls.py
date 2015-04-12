# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.conf.urls import url
from django_comments_threaded.api import views


RE_CONTENT_OBJECT = r'(?P<content_type>\d+)/(?P<object_pk>\d+)/'


urlpatterns = [
    url(RE_CONTENT_OBJECT + '$', views.CreateView.as_view(),
        name='api_create'),
    url(RE_CONTENT_OBJECT + 'flat/$', views.ListView.as_view(),
        name='api_list_flat'),
    url(RE_CONTENT_OBJECT + 'tree/$', views.TreeView.as_view(),
        name='api_list_tree'),
]
