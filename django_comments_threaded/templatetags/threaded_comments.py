# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import template
# from classytags.core import Tag, Options
# from classytags.core import Options
# from classytags.arguments import Argument, KeywordArgument
# from classytags.helpers import InclusionTag, AsTag


register = template.Library()


@register.assignment_tag
def get_comment_list(content_object):
    return Comment.objects.get_for_object(content_object)
