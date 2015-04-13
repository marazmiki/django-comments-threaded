# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.conf.urls import url
from posts import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(),
        name='index'),
    url(r'^posts/$', views.PostListView.as_view(),
        name='post_list'),
    url(r'^posts/(?P<pk>\d+)/$', views.PostDetailView.as_view(),
        name='post_detail'),
    url(r'^links/$', views.LinkListView.as_view(),
        name='link_list'),
    url(r'^images/(?P<pk>\d+)/$', views.LinkDetailView.as_view(),
        name='link_detail'),
]
