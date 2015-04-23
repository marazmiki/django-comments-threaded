# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.db import models
from django_comments_threaded.models import AbstractComment
from six.moves.urllib import request, parse, error


TYPOGRAPH_URL = 'http://www.typograf.ru/webservice/'


class CustomComment(AbstractComment):
    website = models.URLField('Site')


def typograph(**kwargs):
    comment = kwargs['instance']
    params = parse.urlencode({'text': comment.message})

    try:
        with request.urlopen(TYPOGRAPH_URL, params) as fp:
            comment.message = fp.read()
    except (error.URLError, ):
        pass


models.signals.pre_save.connect(typograph, sender=CustomComment,
                                dispatch_uid='custom_comments.models')
