# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import test
from django_comments_threaded.utils import get_model
from django_comments_threaded.tests import Post


Comment = get_model()


class TestPublicManagerMethod(test.TestCase):
    def setUp(self):
        self.post = Post.objects.create()
        self.good = Comment.objects.create(content_object=self.post,
                                           is_moderated=True,
                                           is_spam=False)
        self.bad = Comment.objects.create(content_object=self.post,
                                          is_spam=False,
                                          is_moderated=False)
        self.ugly = Comment.objects.create(content_object=self.post,
                                           is_spam=True,
                                           is_moderated=False)

    def test_count_total(self):
        self.assertEqual(3, Comment.objects.get_for_object(self.post).count())

    def test_public(self):
        self.assertEqual(
            self.good,
            Comment.objects.get_for_object(self.post).public().get()
        )


class TestSpamManagerMethod(test.TestCase):
    def setUp(self):
        self.post = Post.objects.create()
        self.good_comment = Comment.objects.create(content_object=self.post)
        self.bad_comment = Comment.objects.create(content_object=self.post,
                                                  is_spam=True)

    def test_count_total(self):
        self.assertEqual(2, Comment.objects.get_for_object(self.post).count())

    def test_spam(self):
        self.assertEqual(
            self.bad_comment,
            Comment.objects.get_for_object(self.post).spam().get()
        )


class TestInModerationManagerMethod(test.TestCase):
    def setUp(self):
        self.post = Post.objects.create()
        self.good_comment = Comment.objects.create(content_object=self.post,
                                                   is_moderated=True)
        self.bad_comment = Comment.objects.create(content_object=self.post,
                                                  is_moderated=False)

    def test_count_total(self):
        self.assertEqual(2, Comment.objects.get_for_object(self.post).count())

    def test_in_moderation(self):
        self.assertEqual(
            self.bad_comment,
            Comment.objects.get_for_object(self.post).in_moderation().get()
        )
