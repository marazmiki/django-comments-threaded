# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from django_comments.plugins import BasePlugin
from django_comments_threaded.models import Comment
from django_comments_threaded.forms import CommentForm, CommentReplyForm
from django_comments_threaded.views import CreateView, UpdateCommentsView

class ThreadedCommentPlugin(BasePlugin):
    codename = 'threaded'
    content_object_field = 'content_object'

    def get_model(self, request):
        """
        Returns the comment model class
        """
        return Comment

    def get_queryset(self, request, object):
        """
        """
        return self.get_model(request).objects.filter(content_object=object)

    def get_form(self, request, kwargs={}):
        """
        Returns the habrahabr comment ModelForm class
        """
        return CommentReplyForm if 'pk' in kwargs else CommentForm

    def get_urlpatterns(self):
        """
        Returns plugin URLConf
        """
        return patterns('',
            url('^create/$',            CreateView.as_view(plugin=self), name='threaded_comments_create'), 
            url('^reply/(?P<pk>\d+)/$', CreateView.as_view(plugin=self), name='threaded_comments_reply'),
            url('^update/(?P<content_type>\d+)/(?P<object_pk>\d+)/$', UpdateCommentsView.as_view(plugin=self), name='threaded_comments_update'),
        )