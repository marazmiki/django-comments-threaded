# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import test
from django.core.urlresolvers import reverse
from django_comments_threaded.tests import Post, Image, create_user
from django_comments_threaded.templatetags import comments_threaded_tags as t
from django_comments_threaded.utils import get_model


Comment = get_model()


class TestGetCommentApiUrlsTag(test.TestCase):
    def setUp(self):
        self.post = Post.objects.create()

    def test_api(self):
        api = t.get_comment_api_urls(self.post)
        rev = t.r(self.post)
        self.assertEqual(api['list_create'], reverse('api_list_create',
                                                     kwargs=rev))
        self.assertEqual(api['tree'], reverse('api_list_tree', kwargs=rev))


class TestGetCommentListTag(test.TestCase):
    def setUp(self):
        self.post = Post.objects.create()
        self.image = Image.objects.create()
        self.comment = Comment.objects.create(content_object=self.post)
        self.comment_image = Comment.objects.create(content_object=self.image)

    def test_api(self):
        qset = t.get_comment_list(self.post)
        self.assertEqual(1, qset.count())
        self.assertIn(self.comment, qset)

    def test_api_exclude(self):
        qset = t.get_comment_list(self.image)
        self.assertIn(self.comment_image, qset)
        self.assertNotIn(self.comment, qset)


class TestGetCommentFormTag(test.TestCase):
    def setUp(self):
        self.user = create_user()
        self.post = Post.objects.create()
        self.req = test.RequestFactory()

    def test_get(self):
        form = t.get_comment_form({'request': self.req.get('/')}, self.post)
        print(form)

    def test_post(self):
        form = t.get_comment_form({'request': self.req.post('/', {})},
                                  self.post)
        print(form)

# get_comment_api_urls(content_object, **kwargs):
# get_comment_list(content_object, **kwargs):
# def get_comment_form(context, content_object, **kwargs):
