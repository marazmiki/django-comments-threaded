# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.db import models
from django_comments_threaded.models import AbstractComment


class CustomComment(AbstractComment):
    website = models.URLField('Site')
