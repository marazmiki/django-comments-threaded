# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from rest_framework.serializers import ModelSerializer, CharField
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django_comments_threaded.models import Comment, LastRead


class RequestMixin(object):
    def get_context_kwargs(self, key):
        return self.context['view'].kwargs[key]

    def get_request(self):
        return self.context['request']

    @property
    def request(self):
        return self.get_request()


class CommentSerializer(RequestMixin, ModelSerializer):
    message = CharField(required=True)

    def create(self, validated_data):
        validated_data.update(
            object_pk=self.get_context_kwargs('object_pk'),
            content_type_id=self.get_context_kwargs('content_type'),
        )
        return Comment.objects.create(**validated_data)

    class Meta(object):
        model = Comment
        exclude = ['content_type', 'object_pk', 'is_active', 'user',
                   'is_spam', 'is_moderated', 'parent', 'remote_addr']


class CommentReplySerializer(RequestMixin, ModelSerializer):
    message = CharField(required=True)

    def create(self, validated_data):
        parent = Comment.objects.get(pk=self.get_context_kwargs('pk'))
        validated_data.update(
            content_object=parent.content_object,
            parent=parent
        )
        return Comment.objects.create(**validated_data)

    class Meta(CommentSerializer.Meta):
        pass


class LastReadSerializer(ModelSerializer):
    class Meta(object):
        model = LastRead
