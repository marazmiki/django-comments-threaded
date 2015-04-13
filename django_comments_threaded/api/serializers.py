# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from rest_framework.serializers import ModelSerializer
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
    def create(self, validated_data):
        validated_data.update(
            object_pk=self.get_context_kwargs('object_pk'),
            content_type_id=self.get_context_kwargs('content_type'),
        )
        return Comment.objects.create(**validated_data)

    class Meta(object):
        model = Comment
        write_only_fields = ['message']
        exclude = ['content_type', 'object_pk', 'is_active',
                   'is_spam', 'is_moderated']


class LastReadSerializer(ModelSerializer):
    class Meta(object):
        model = LastRead
