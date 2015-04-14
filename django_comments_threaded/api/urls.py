# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.conf.urls import url
from django_comments_threaded.api import views


RE_CONTENT_OBJECT = r'(?P<content_type>\d+)/(?P<object_pk>\d+)/'


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.ReplyView.as_view(),
        name='api_reply'),
    url(r'^' + RE_CONTENT_OBJECT + '$', views.ListCreateView.as_view(),
        name='api_list_create'),
    url(r'^' + RE_CONTENT_OBJECT + 'tree/$', views.TreeView.as_view(),
        name='api_list_tree'),
]
