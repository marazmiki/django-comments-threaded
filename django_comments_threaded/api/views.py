# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from rest_framework import generics
from rest_framework.response import Response
from django_comments_threaded.models import Comment
from django_comments_threaded.api import serializers
from django_comments_threaded.api.utils import to_tree


class CommentMixin(object):
    serializer_class = serializers.CommentSerializer

    def content_object_filter(self):
        return {
            'content_type_id': self.kwargs['content_type'],
            'object_pk': self.kwargs['object_pk'],
        }

    def get_queryset(self):
        return Comment.objects.filter(**self.content_object_filter())


class ReplyView(CommentMixin, generics.CreateAPIView):
    serializer_class = serializers.CommentReplySerializer


class ListCreateView(CommentMixin, generics.ListCreateAPIView):
    pass


class TreeView(CommentMixin, generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        return Response(to_tree(self.get_queryset()))
