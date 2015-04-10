# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CommentsThreadedAPIConfig(AppConfig):
    name = 'django_comments_threaded.api'
    verbose_name = _('comments')
