# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import test
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from generic_helpers.utils import ct
from django_comments_threaded.tests import Post
from django_comments_threaded.utils import get_model
from django_comments_threaded.signals import comment_created, comment_replied
import urlparse


User = get_user_model()
Comment = get_model()


def create_user(username='user', email='user@example.com', password='user'):
    user = User.objects.create_user(username=username, email=email,
                                    password=password)
    user.credentials = {
        'username': user.username,
        'password': password
    }
    return user


def signal_handler(**kwargs):
    raise SignalFired()


class SignalFired(Exception):
    pass


class TestCommentCreateView(test.TestCase):
    def setUp(self):
        self.url = reverse('threaded_comments_create')
        self.user = create_user()
        self.post = Post.objects.create()
        self.client = test.Client()
        self.client.login(**self.user.credentials)

    def test_signal_fired(self):
        comment_created.connect(signal_handler, sender=Comment)
        with self.assertRaises(SignalFired):
            self.client.post(self.url, {
                'message': 'Test comment',
                'user_name': 'Anonymous',
                'user_email': 'anonymous@example.com',
                'content_type': ct(self.post).pk,
                'object_pk': self.post.pk,
            })
        comment_created.disconnect(signal_handler, sender=Comment)

    def test_anonymous_user_create_comment(self):
        self.client.logout()
        self.client.post(self.url, {
            'message': 'Test comment',
            'user_name': 'Anonymous',
            'user_email': 'anonymous@example.com',
            'content_type': ct(self.post).pk,
            'object_pk': self.post.pk,
        })

        comment = Comment.objects.get()

        self.assertIsNone(comment.parent)
        self.assertIsNone(comment.user)
        self.assertEqual('Test comment', comment.message)
        self.assertEqual('Anonymous', comment.user_name)
        self.assertEqual('anonymous@example.com', comment.user_email)

    def test_success_redirect_when_content_object_hasnt_absolute_url(self):
        resp = self.client.post(self.url, {
            'message': 'Test comment',
            'user_name': 'Anonymous',
            'user_email': 'anonymous@example.com',
            'content_type': ct(self.post).pk,
            'object_pk': self.post.pk,
        })
        self.assertEqual('/', urlparse.urlparse(resp['location']).path)

    def test_success_redirect_when_content_object_has_absolute_url(self):
        Post.get_absolute_url = lambda s: '/foo/'

        resp = self.client.post(self.url, {
            'message': 'Test comment',
            'user_name': 'Anonymous',
            'user_email': 'anonymous@example.com',
            'content_type': ct(self.post).pk,
            'object_pk': self.post.pk,
        })

        self.assertEqual('/foo/', urlparse.urlparse(resp['location']).path)
        del Post.get_absolute_url

    def test_authenticated_user_create_comment(self):
        self.client.post(self.url, {
            'message': 'Test comment',
            'user_name': 'Anonymous',
            'user_email': 'anonymous@example.com',
            'content_type': ct(self.post).pk,
            'object_pk': self.post.pk,
        })

        comment = Comment.objects.get()

        self.assertIsNone(comment.parent)
        self.assertEqual(self.user, comment.user)
        self.assertEqual('Test comment', comment.message)
        self.assertEqual('Anonymous', comment.user_name)
        self.assertEqual('anonymous@example.com', comment.user_email)


class TestCommentReplyView(test.TestCase):
    def setUp(self):
        self.user = create_user()
        self.post = Post.objects.create()
        self.parent = Comment.objects.create(content_object=self.post)
        self.url = reverse('threaded_comments_reply', args=[self.parent.pk])
        self.client = test.Client()
        self.client.login(**self.user.credentials)

    def test_anonymous_user_reply_comment(self):
        self.client.logout()
        self.client.post(self.url, {
            'message': 'Test comment',
            'user_name': 'Anonymous',
            'user_email': 'anonymous@example.com',
        })

        comment = self.parent.replies.get()

        self.assertIsNone(comment.user)
        self.assertEqual(self.parent, comment.parent)
        self.assertEqual('Test comment', comment.message)
        self.assertEqual('Anonymous', comment.user_name)
        self.assertEqual('anonymous@example.com', comment.user_email)

    def test_success_redirect_when_content_object_hasnt_absolute_url(self):
        resp = self.client.post(self.url, {
            'message': 'Test comment',
            'user_name': 'Anonymous',
            'user_email': 'anonymous@example.com',
            'content_type': ct(self.post).pk,
            'object_pk': self.post.pk,
        })
        self.assertEqual('/', urlparse.urlparse(resp['location']).path)

    def test_success_redirect_when_content_object_has_absolute_url(self):
        Post.get_absolute_url = lambda s: '/foo/'

        resp = self.client.post(self.url, {
            'message': 'Test comment',
            'user_name': 'Anonymous',
            'user_email': 'anonymous@example.com',
            'content_type': ct(self.post).pk,
            'object_pk': self.post.pk,
        })

        self.assertEqual('/foo/', urlparse.urlparse(resp['location']).path)
        del Post.get_absolute_url

    def test_authenticated_user_reply_comment(self):
        self.client.post(self.url, {
            'message': 'Test comment',
            'user_name': 'Anonymous',
            'user_email': 'anonymous@example.com',
            'content_type': ct(self.post).pk,
            'object_pk': self.post.pk,
        })

        comment = self.parent.replies.get()

        self.assertEqual(self.user, comment.user)
        self.assertEqual(self.parent, comment.parent)
        self.assertEqual('Test comment', comment.message)
        self.assertEqual('Anonymous', comment.user_name)
        self.assertEqual('anonymous@example.com', comment.user_email)

    def test_signal_fired(self):
        comment_replied.connect(signal_handler, sender=Comment)
        with self.assertRaises(SignalFired):
            self.client.post(self.url, {
                'message': 'Test comment',
                'user_name': 'Anonymous',
                'user_email': 'anonymous@example.com',
                'content_type': ct(self.post).pk,
                'object_pk': self.post.pk,
            })
        comment_replied.disconnect(signal_handler, sender=Comment)
