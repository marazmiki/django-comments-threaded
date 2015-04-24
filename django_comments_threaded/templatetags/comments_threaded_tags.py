# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import template
from django.core.urlresolvers import reverse
from generic_helpers.managers import ct
from django_comments_threaded.utils import get_create_form, get_model


register = template.Library()


def r(content_object):
    return {
        'content_type': ct(content_object).pk,
        'object_pk': content_object.pk,
    }


@register.assignment_tag
def get_comment_api_urls(content_object, **kwargs):
    rev = r(content_object)
    return {
        'list_create': reverse('api_list_create', kwargs=rev),
        'tree': reverse('api_list_tree', kwargs=rev)
    }


@register.assignment_tag
def get_comment_list(content_object, **kwargs):
    return get_model().objects.get_for_object(content_object)


@register.assignment_tag(takes_context=True)
def get_comment_form(context, content_object, **kwargs):
    request = context['request']
    return get_create_form()(request.POST or None,
                             request.FILES or None,
                             initial=r(content_object))
