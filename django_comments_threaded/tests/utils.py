# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import test
from django.core.exceptions import ImproperlyConfigured
from django_comments_threaded.forms import CommentReplyForm, CommentCreateForm
from django_comments_threaded.models import Comment
from django_comments_threaded.tests import Image
from django_comments_threaded.utils import (get_model, get_reply_form,
                                            get_create_form)


class TestGetModel(test.TestCase):
    def test_default(self):
        self.assertEquals(Comment, get_model())

    def test_custom_model(self):
        custom_cls = 'django_comments_threaded.tests.Image'
        with self.settings(THREADED_COMMENTS_MODEL=custom_cls):
            self.assertEquals(Image, get_model())

    def test_non_exist_model_class(self):
        with self.assertRaises(ImproperlyConfigured), \
                self.settings(THREADED_COMMENTS_MODEL='not.exists.Model'):
            get_model()


class TestGetCreateForm(test.TestCase):
    def test_default(self):
        self.assertEquals(CommentCreateForm, get_create_form())

    def test_custom_create_form(self):
        custom_cls = 'django_comments_threaded.tests.Image'

        with self.settings(THREADED_COMMENTS_CREATE_FORM=custom_cls):
            self.assertEquals(Image, get_create_form())

    def test_non_exist_create_form_class(self):
        with self.assertRaises(ImproperlyConfigured):
            with self.settings(THREADED_COMMENTS_CREATE_FORM='bad.Form'):
                get_create_form()


class TestGetReplyForm(test.TestCase):
    def test_default(self):
        self.assertEquals(CommentReplyForm, get_reply_form())

    def test_custom_reply_form(self):
        custom_cls = 'django_comments_threaded.tests.Image'

        with self.settings(THREADED_COMMENTS_REPLY_FORM=custom_cls):
            self.assertEquals(Image, get_reply_form())

    def test_non_exist_reply_form_class(self):
        with self.assertRaises(ImproperlyConfigured), \
                self.settings(THREADED_COMMENTS_REPLY_FORM='bad.Form'):
            get_reply_form()
