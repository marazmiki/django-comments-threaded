# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from mptt.templatetags.mptt_tags import cache_tree_children
from django.core.urlresolvers import reverse
from generic_helpers.managers import ct
from rest_framework import test
from django_comments_threaded.tests import Post, Image
from django_comments_threaded.models import Comment


class TestListView(test.APITestCase):
    def setUp(self):
        self.object_1 = Post.objects.create()
        self.object_2 = Image.objects.create()
        self.client = test.APIClient()

        for i in [self.object_1, self.object_2]:
            parent = None
            for j in range(1, 11):
                parent = Comment.objects.create(content_object=i,
                                       message='Comment {}'.format(j),
                                       parent=parent)
                if j and not j % 6:
                    parent = None

    def get_absolute_url(self, content_object):
        return reverse('api_list_flat', kwargs={
            'content_type': ct(content_object).pk,
            'object_pk': content_object.pk
        })

    def test_1(self):
        resp = self.client.get(self.get_absolute_url(self.object_1))
        self.assertEqual(20, Comment.objects.count())
        self.assertEqual(10, len(resp.data))

        rr = reverse('api_list_tree', kwargs={
            'content_type': ct(self.object_1).pk,
            'object_pk': self.object_1.pk
        })

        resp = self.client.get(rr)
        print(resp)
