# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Post(models.Model):
    text = models.TextField(default='')

    def __str__(self):
        return self.text

    @models.permalink
    def get_absolute_url(self):
        return 'post_detail', [self.pk]


@python_2_unicode_compatible
class Link(models.Model):
    url = models.URLField(default='')

    def __str__(self):
        return self.url

    @models.permalink
    def get_absolute_url(self):
        return 'link_detail', [self.pk]
