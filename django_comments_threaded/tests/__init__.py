# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import test
from django.db import models
from django.conf.urls import url, include
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    pass


class Image(models.Model):
    pass


def create_user(username='user', email='user@example.com', password='user'):
    user = User.objects.create_user(username=username, email=email,
                                    password=password)
    user.credentials = {
        'username': user.username,
        'password': password
    }
    return user


urlpatterns = [
    url(r'^comments/', include('django_comments_threaded.urls')),
]

# __init__

from django_comments_threaded import get_version

# admin
from django_comments_threaded import admin    # NOQA


class TestGetVersion(test.TestCase):
    def test_1(self):
        self.assertEqual('1.0.0', get_version())


# models
from django_comments_threaded.tests.models import (
    TestStrCommentMethod, TestGetReplyUrlCommentMethod,
    TestSoftDeleteCommentMethod, TestHasRepliesCommentMethod,
    TestCountRepliesCommentMethod, TestStrLastReadMethod
)

# managers
from django_comments_threaded.tests.managers import (
    TestSpamManagerMethod, TestInModerationManagerMethod,
    TestPublicManagerMethod
)

# templatetags
from django_comments_threaded.tests.templatetags import (
    TestGetCommentApiUrlsTag, TestGetCommentListTag, TestGetCommentFormTag
)

# utils
from django_comments_threaded.tests.utils import (TestGetModel,
                                                  TestGetCreateForm,
                                                  TestGetReplyForm)
# views
from django_comments_threaded.tests.views import (TestCommentCreateView,
                                                  TestCommentReplyView)

__all__ = [
    'TestGetVersion',
    'TestGetModel', 'TestGetCreateForm', 'TestGetReplyForm',
    'TestSpamManagerMethod', 'TestInModerationManagerMethod',
    'TestPublicManagerMethod',
    'TestCommentCreateView', 'TestCommentReplyView',
    'TestStrCommentMethod', 'TestGetReplyUrlCommentMethod',
    'TestSoftDeleteCommentMethod', 'TestHasRepliesCommentMethod',
    'TestCountRepliesCommentMethod', 'TestStrLastReadMethod',
    'TestGetCommentApiUrlsTag', 'TestGetCommentListTag',
    'TestGetCommentFormTag',
]
