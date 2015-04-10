# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from django_comments_threaded.models import Comment
from django_comments_threaded.api.serializers import CommentSerializer
from mptt.templatetags.mptt_tags import cache_tree_children


def recursive_node_to_dict(node):
    result = {
        'id': node.pk,
        'name': node.name,
    }
    children = [recursive_node_to_dict(c) for c in node.get_children()]
    if children:
        result['children'] = children
    return result


class ListView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            content_type=self.kwargs['content_type'],
            object_pk=self.kwargs['object_pk']
        )


class TreeView(ListView):
    # def list(self, request, *args, **kwargs):
    #     # queryset = self.filter_queryset(self.get_queryset())
    #     #
    #     # page = self.paginate_queryset(queryset)
    #     # if page is not None:
    #     #     serializer = self.get_serializer(page, many=True)
    #     #     return self.get_paginated_response(serializer.data)
    #     #
    #     # serializer = self.get_serializer(queryset, many=True)
    #
    #
    # root_nodes = cache_tree_children(Node.objects.all())
    # dicts = []
    # for n in root_nodes:
    #     dicts.append(recursive_node_to_dict(n))
    #
    #
    #     return Response(serializer.data)
    pass
