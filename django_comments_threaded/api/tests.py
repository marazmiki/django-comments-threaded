# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.core.urlresolvers import reverse
from generic_helpers.managers import ct
from rest_framework import test
from django_comments_threaded.tests import Post, create_user
from django_comments_threaded.utils import get_model
from django_comments_threaded.api.permissions import CanDeleteOwnComment
import datetime


Comment = get_model()


def create_comments_tree(content_object, num):
    parent = None

    for j in range(1, num + 1):
        parent = Comment.objects.create(
            content_object=content_object,
            message='Comment #{}'.format(j),
            parent=parent)
        if j and not j % 6:
            parent = None


class BaseTest(test.APITestCase):
    view_name = ''

    def setUp(self):
        self.content_object = Post.objects.create()
        self.client = test.APIClient()
        create_comments_tree(self.content_object, 10)

    def get_absolute_url(self, content_object=None):
        content_object = content_object or self.content_object
        return reverse(self.view_name, kwargs={
            'content_type': ct(content_object).pk,
            'object_pk': content_object.pk
        })


class TestListView(BaseTest):
    view_name = 'api_list_create'

    def test_simple(self):
        resp = self.client.get(self.get_absolute_url())
        self.assertEqual(10, len(resp.data))


class TestTreeView(BaseTest):
    view_name = 'api_list_tree'

    def test_1(self):
        resp = self.client.get(self.get_absolute_url())
        import json
        from django.core.serializers.json import DjangoJSONEncoder
        json.dumps(resp.data, indent=2, cls=DjangoJSONEncoder)


class TestCreateView(test.APITestCase):
    view_name = 'api_list_create'

    def setUp(self):
        self.content_object = Post.objects.create()
        self.client = test.APIClient()

    def get_absolute_url(self, content_object=None):
        content_object = content_object or self.content_object
        return reverse(self.view_name, kwargs={
            'content_type': ct(content_object).pk,
            'object_pk': content_object.pk
        })

    def test_(self):
        self.client.post(self.get_absolute_url(), data={'message': 'Message'})

        comment = Comment.objects.get()

        self.assertEqual('Message', comment.message)
        self.assertEqual(self.content_object, comment.content_object)
        self.assertIsNone(comment.parent)


class TestReplyView(test.APITestCase):
    view_name = 'api_reply'

    def setUp(self):
        self.post = Post.objects.create()
        self.user = create_user()
        self.comment = Comment.objects.create(content_object=self.post,
                                              user=self.user)
        self.url = reverse(self.view_name, kwargs={'pk': self.comment.pk})
        self.another_user = create_user(username='another_user')
        self.client = test.APIClient()
        self.client.login(**self.user.credentials)

    def assertCommentDeleted(self, resp):
        self.assertEqual(204, resp.status_code)
        self.assertEqual(0, Comment.objects.public().count())

    def test_200(self):
        self.client.post(self.url, data={'message': 'Reply'})

        reply = self.comment.replies.get()

        self.assertEqual('Reply', reply.message)
        self.assertEqual(self.comment, reply.parent)

    def test_400_if_empty_message(self):
        resp = self.client.post(self.url, data={'message': ''})
        self.assertEqual(400, resp.status_code)
        self.assertIn('message', resp.data)

    def test_400_if_empty_data(self):
        resp = self.client.post(self.url, data=None)
        self.assertEqual(400, resp.status_code)
        self.assertIn('message', resp.data)

    def test_delete_anonymous(self):
        self.client.logout()
        self.assertEqual(403, self.client.delete(self.url).status_code)

    def test_delete_authenticated_no_owner(self):
        self.client.logout()
        self.client.login(**create_user(username='user_2').credentials)
        self.assertEqual(403, self.client.delete(self.url).status_code)

    def test_delete_when_superuser(self):
        self.user.is_superuser = True
        self.user.save()
        self.assertCommentDeleted(self.client.delete(self.url))

    def test_delete_when_own(self):
        self.user.is_superuser = False
        self.user.save()
        self.assertCommentDeleted(self.client.delete(self.url))

    def test_delete_failure_(self):
        self.comment.date_created = datetime.date(2011, 2, 11)
        self.comment.save()
        self.user.is_superuser = False
        self.user.save()
        self.assertEqual(403, self.client.delete(self.url).status_code)

    def test_delete_http_method_smoke_test(self):
        class Request(object):
            method = 'GET'

        perm = CanDeleteOwnComment()
        self.assertTrue(perm.has_object_permission(Request(), None, None))
