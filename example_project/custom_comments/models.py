# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_comments_threaded.models import AbstractComment
import requests
import requests.exceptions


TYPOGRAPH_URL = 'http://www.typograf.ru/webservice/'


class CustomComment(AbstractComment):
    """
    Customized threaded comments model
    """
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
    try:
        comment.message = requests.post(TYPOGRAPH_URL, {
            'text': comment.message,
            'chr': 'UTF-8'
        }).content.decode('utf-8')
    except Exception as e:
        print(e, type(e))
        pass


models.signals.pre_save.connect(typograph, sender=CustomComment,
                                dispatch_uid='custom_comments.models')
