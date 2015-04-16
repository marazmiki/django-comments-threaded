# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import test
from django.utils import six
from django.core.urlresolvers import reverse, NoReverseMatch
from django_comments_threaded.tests import Post, Image, create_user
from django_comments_threaded.models import LastRead, Comment


s = six.text_type


class TestStrCommentMethod(test.TestCase):
    def test_short(self):
        self.assertEqual('Hello world', s(Comment(message='Hello world')))

    def test_long(self):
        self.assertEqual(
            s('Lorem ipsum dolor sit amet, co...'),
            s(Comment(message='Lorem ipsum dolor sit amet, consectetur')))


class TestGetReplyUrlCommentMethod(test.TestCase):
    def test_saved_comment(self):
        self.assertEqual(reverse('threaded_comments_reply', args=[1]),
                         Comment(pk=1).get_reply_url())

    def test_empty_url_when_comment_not_saved(self):
        with self.assertRaises(NoReverseMatch):
            Comment(pk=None).get_reply_url()


class TestSoftDeleteCommentMethod(test.TestCase):
    def setUp(self):
        self.post = Post.objects.create()
        self.comment = Comment.objects.create(content_object=self.post,
                                              is_active=True)

    def test_soft_delete(self):
        self.comment.soft_delete()
        self.assertFalse(self.comment.is_active)

    def test_soft_delete_manager(self):
        self.assertIn(self.comment, Comment.objects.public())
        self.comment.soft_delete()
        self.assertNotIn(self.comment, Comment.objects.public())


class TestHasRepliesCommentMethod(test.TestCase):
    def setUp(self):
        self.post = Post.objects.create()
        self.comment = Comment.objects.create(content_object=self.post)

    def test_count_replies_no(self):
        self.assertFalse(self.comment.has_replies())

    def test_count_replies_yes(self):
        Comment.objects.create(content_object=self.post, parent=self.comment)
        Comment.objects.create(content_object=self.post, parent=self.comment)
        self.assertTrue(self.comment.has_replies())


class TestCountRepliesCommentMethod(test.TestCase):
    def setUp(self):
        self.post = Post.objects.create()
        self.comment = Comment.objects.create(content_object=self.post)

    def test_count_replies(self):
        self.assertEqual(0, self.comment.count_replies())

    def test_count_replies_flat(self):
        Comment.objects.create(content_object=self.post,
                               parent=self.comment)
        Comment.objects.create(content_object=self.post,
                               parent=self.comment)
        self.assertEqual(2, self.comment.count_replies())

    def test_count_replies_tree(self):
        Comment.objects.create(
            content_object=self.post,
            parent=Comment.objects.create(content_object=self.post,
                                          parent=self.comment)
        )
        self.assertEqual(2, self.comment.count_replies())

    def test_count_replies_combined(self):
        Comment.objects.create(
            content_object=self.post,
            parent=self.comment
        )
        Comment.objects.create(
            content_object=self.post,
            parent=Comment.objects.create(content_object=self.post,
                                          parent=self.comment)
        )
        self.assertEqual(3, self.comment.count_replies())


class TestStrLastReadMethod(test.TestCase):
    def setUp(self):
        self.post = Image.objects.create()
        self.user = create_user(username='god')

    def test_it(self):
        self.assertEqual(s('god has read Image object'),
                         s(LastRead(user=self.user, content_object=self.post)))
