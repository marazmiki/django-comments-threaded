# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.core.urlresolvers import reverse
from generic_helpers.managers import ct
from rest_framework import test
from django_comments_threaded.tests import Post
from django_comments_threaded.models import Comment


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
    view_name = 'api_list_flat'

    def test_simple(self):
        resp = self.client.get(self.get_absolute_url())
        self.assertEqual(10, len(resp.data))


class TestTreeView(BaseTest):
    view_name = 'api_list_tree'

    def test_1(self):
        resp = self.client.get(self.get_absolute_url())
        import json
        from django.core.serializers.json import DjangoJSONEncoder

        print(json.dumps(resp.data, indent=2, cls=DjangoJSONEncoder))


class TestCreateView(test.APITestCase):
    def setUp(self):
        pass
