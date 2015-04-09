# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


VERSION = (1, 0, 0)
default_app_config = 'django_comments_threaded.apps.CommentsThreadedConfig'


def get_version():
    try:
        unicode
    except NameError:
        unicode = str
    return '.'.join(map(unicode, VERSION))
