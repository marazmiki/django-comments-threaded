# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from mptt.templatetags.mptt_tags import cache_tree_children
from django_comments_threaded.api.serializers import CommentSerializer


def expand_node(node, children_key='replies'):
    result = CommentSerializer(node)
    data = result.data.copy()
    children = [expand_node(c) for c in node.get_children()]

    if children:
        data.update(children_key=children)
    return data


def to_tree(queryset):
    return [expand_node(n) for n in cache_tree_children(queryset)]
