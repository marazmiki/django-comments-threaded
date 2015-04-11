# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from django_comments_threaded.models import Comment
from django_comments_threaded.api.serializers import CommentSerializer
from django_comments_threaded.api.utils import to_tree


class CreateView(CreateAPIView):
    serializer_class = CommentSerializer


class ListView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            content_type=self.kwargs['content_type'],
            object_pk=self.kwargs['object_pk']
        )


class TreeView(ListView):
    def list(self, request, *args, **kwargs):
        return Response(to_tree(self.get_queryset()))
