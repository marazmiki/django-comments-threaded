# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import test
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

# __init__

from django_comments_threaded import get_version

# admin
from django_comments_threaded import admin    # NOQA


class TestGetVersion(test.TestCase):
    def test_1(self):
        self.assertEqual('1.0.0', get_version())


# utils

from django_comments_threaded.tests.managers import (
    TestSpamManagerMethod, TestInModerationManagerMethod,
    TestPublicManagerMethod
)
from django_comments_threaded.tests.utils import (TestGetModel,
                                                  TestGetCreateForm,
                                                  TestGetReplyForm)
from django_comments_threaded.tests.views import (TestCommentCreateView,
                                                  TestCommentReplyView)

__all__ = [
    'TestGetVersion',
    'TestGetModel', 'TestGetCreateForm', 'TestGetReplyForm',
    'TestSpamManagerMethod', 'TestInModerationManagerMethod',
    'TestPublicManagerMethod',
    'TestCommentCreateView', 'TestCommentReplyView',
]
