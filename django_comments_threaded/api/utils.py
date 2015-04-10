# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from mptt.templatetags.mptt_tags import cache_tree_children


def recursive_node_to_dict(node, children_key='replies'):
    result = {k: v for k, v in node.__dict__.items() if not k.startswith('_')}

    children = [recursive_node_to_dict(c) for c in node.get_children()]

    if children:
        result[children_key] = children
    return result


def to_tree(queryset):
    return [recursive_node_to_dict(n) for n in cache_tree_children(queryset)]
