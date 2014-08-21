# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

VERSION = (0, 2, 0, 'a')
codename = 'threaded'
default_app_config = 'django_comments_threaded.apps.CommentsThreadedConfig'


def get_version():
    return '.'.join(map(unicode, VERSION))