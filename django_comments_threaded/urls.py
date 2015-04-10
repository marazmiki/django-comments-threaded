# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.conf.urls import url
from django_comments.views import (CreateCommentView, ReplyCommentView,
                                   LastReadView, MarkReadView)


urlpatterns = [
    url(r'^create/$', 
        view=CreateCommentView.as_view(),
        name='threaded_comments_create'),
    url(r'^reply/(?P<pk>\d+)/$',
        view=ReplyCommentView.as_view(),
        name='threaded_comments_reply'),
    url(r'^fresh/(?P<content_type>\d+)/(?P<object_pk>\d+)/$', 
        view=LastReadView.as_view(),
        name='threaded_comments_get_new'),
    url(r'^mark/(?P<content_type>\d+)/(?P<object_pk>\d+)/$',
        view=MarkReadView.as_view(),
        name='thread_comments_mark_read')
]
