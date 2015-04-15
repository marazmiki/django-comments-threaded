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


class TestCommentCreateView(test.TestCase):
    def setUp(self):
        self.url = reverse('threaded_comments_create')
        self.user = create_user()
        self.post = Post.objects.create()
        self.client = test.Client()
        self.client.login(**self.user.credentials)

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

        self.assertIsNone(comment.user)
        self.assertEqual('Test comment', comment.message)
        self.assertEqual('Anonymous', comment.user_name)
        self.assertEqual('anonymous@example.com', comment.user_email)

    def test_content_object_without_absolute_url(self):
        resp = self.client.post(self.url, {
            'message': 'Test comment',
            'user_name': 'Anonymous',
            'user_email': 'anonymous@example.com',
            'content_type': ct(self.post).pk,
            'object_pk': self.post.pk,
        })
        self.assertRedirects(resp, expected_url='/')

    def test_authenticated_user_create_comment(self):
        self.client.post(self.url, {
            'message': 'Test comment',
            'user_name': 'Anonymous',
            'user_email': 'anonymous@example.com',
            'content_type': ct(self.post).pk,
            'object_pk': self.post.pk,
        })

        comment = Comment.objects.get()

        self.assertEqual(self.user, comment.user)
        self.assertEqual('Test comment', comment.message)
        self.assertEqual('Anonymous', comment.user_name)
        self.assertEqual('anonymous@example.com', comment.user_email)



class TestCommentReplyView(test.TestCase):
    pass
