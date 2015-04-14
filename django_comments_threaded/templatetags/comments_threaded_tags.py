# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import template
from django.core.urlresolvers import reverse
from generic_helpers.managers import ct
from django_comments_threaded.models import Comment


register = template.Library()


@register.assignment_tag
def get_comment_api_urls(content_object, **kwargs):
    rev = {
        'content_type': ct(content_object).pk,
        'object_pk': content_object.pk,
    }
    return {
        'list_create': reverse('api_list_create', kwargs=rev),
        'tree': reverse('api_list_tree', kwargs=rev)
    }

@register.assignment_tag
def get_comment_list(content_object, **kwargs):
    return Comment.objects.get_for_object(content_object)
