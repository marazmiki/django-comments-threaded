# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.db import models
from django.conf.urls import url, include
from django.shortcuts import render


class Post(models.Model):
    pass


class Image(models.Model):
    pass


def index(request):
    cntx = {
    }
    return render(request, 'django_comments_threaded/tests/index.html', cntx)


urlpatterns = [
    url(r'^$', index),
    url(r'^comments/', include('django_comments_threaded.urls')),
]


# utils

from django_comments_threaded.tests.utils import (TestGetModel)


__all__ = ['TestGetModel']
