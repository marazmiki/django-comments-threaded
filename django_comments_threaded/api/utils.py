# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from mptt.templatetags.mptt_tags import cache_tree_children


def expand_node(node, children_key='replies', exclude=None):
    result = {k: v for k, v in node.__dict__.items() if not k.startswith('_')}

    if exclude:
        result = {k: v for k, v in result.items() if k not in exclude}

    children = [expand_node(c) for c in node.get_children()]

    if children:
        result[children_key] = children
    return result


def to_tree(queryset):
    from django_comments_threaded.api.serializers import CommentSerializer
    ex = CommentSerializer.Meta.write_only_fields
    return [expand_node(n, exclude=ex) for n in cache_tree_children(queryset)]
