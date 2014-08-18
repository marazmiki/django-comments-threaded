# coding: utf-8

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
import json


def json_response(data, indent=None, ensure_ascii=True):
    """
    Creates HttpResponse object with JSON content
    """
    return HttpResponse(content=json.dumps(data, indent=indent,
                                           ensure_ascii=ensure_ascii),
                        content_type='application/x-json')


def get_update_url(content_object):
    """
    Returns URL of page that outputs unreaded comments
    """
    return reverse('threaded_comments_update', kwargs={
        'content_type': ContentType.objects.get_for_model(content_object).pk,
        'object_pk': content_object.pk,
    })
