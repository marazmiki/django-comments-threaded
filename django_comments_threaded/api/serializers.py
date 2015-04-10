# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from rest_framework.serializers import ModelSerializer
from django_comments_threaded.models import Comment, LastRead


class CommentSerializer(ModelSerializer):
    class Meta(object):
        model = Comment


class LastReadSerializer(ModelSerializer):
    class Meta(object):
        model = LastRead
