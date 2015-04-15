# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.core.signals import Signal


comment_created = Signal(providing_args=['comment', 'request'])
comment_replied = Signal(providing_args=['comment', 'parent', 'request'])
