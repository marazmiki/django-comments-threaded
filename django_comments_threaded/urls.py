# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.conf.urls import url, include
from django_comments_threaded import views


regular_urlpatterns = [
    url(r'^create/$',
        view=views.CreateCommentView.as_view(),
        name='threaded_comments_create'),
    url(r'^reply/(?P<pk>\d+)/$',
        view=views.ReplyCommentView.as_view(),
        name='threaded_comments_reply'),
    # url(r'^fresh/(?P<content_type>\d+)/(?P<object_pk>\d+)/$',
    #     view=views.LastReadView.as_view(),
    #     name='threaded_comments_get_new'),
    # url(r'^mark/(?P<content_type>\d+)/(?P<object_pk>\d+)/$',
    #     view=views.MarkReadView.as_view(),
    #     name='thread_comments_mark_read')
]

urlpatterns = [
    url(r'^', include(regular_urlpatterns)),
    url(r'^api/', include('django_comments_threaded.api.urls')),
]
