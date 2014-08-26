# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import test
from django.db import models
from django.conf.urls import url, include
from django.contrib.auth import get_user_model
from django.shortcuts import render


def create_user(username=None, password=None, email=None,
                is_staff=False, is_superuser=False):
    user = get_user_model().objects.create_user(username=username,
                                                password=password,
                                                email=email,
                                                is_staff=is_staff,
                                                is_superuser=is_superuser)
    user.raw_password = password
    return user


class Post(models.Model):
    pass


class Image(models.Model):
    pass


class AnonymousTest(test.TestCase):
    def setUp(self):
        self.post = Post.objects.create()

    def test_1(self):
        pass


def index(request):
    cntx = {
    }
    return render(request, 'django_comments_threaded/tests/index.html', cntx)


urlpatterns = [
    url(r'^$', index),
    url(r'^comments/', include('django_comments_threaded.urls')),
]
