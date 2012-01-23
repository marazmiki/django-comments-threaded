# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

def json_response(data):
    """
    Creates HttpResponse object with JSON content
    """
    return HttpResponse(
        content  = simplejson.dumps(data),
        mimetype = 'application/x-json'
    )

def get_update_url(content_object):
    """
    Returns URL of page that outputs unreaded comments
    """
    return reverse('threaded_comments_update', kwargs={
        'content_type': ContentType.objects.get_for_model(content_object).pk,
        'object_pk': content_object.pk,
    })
