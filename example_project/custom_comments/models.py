# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_comments_threaded.models import AbstractComment
from six.moves.urllib import request, parse, error


TYPOGRAPH_URL = 'http://www.typograf.ru/webservice/'


class CustomComment(AbstractComment):
    DEVICE_DESKTOP = 'desktop'
    DEVICE_MOBILE = 'mobile'
    DEVICE_ANDROID = 'android'
    DEVICE_APPLE = 'apple'

    website = models.URLField('Site')
    device = models.CharField(_('device'),  max_length=25,
                              default=DEVICE_DESKTOP,
                              choices=(
                                  (DEVICE_DESKTOP, _('desktop')),
                                  (DEVICE_ANDROID, _('android')),
                                  (DEVICE_MOBILE, _('mobile')),
                                  (DEVICE_APPLE, _('apple')),
                              ))
                          

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
