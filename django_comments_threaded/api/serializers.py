# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from rest_framework import serializers
from django.db.models import permalink
from django_comments_threaded.models import LastRead
from django_comments_threaded.utils import get_model


class RequestMixin(object):
    def get_context_kwargs(self, key):
        return self.context['view'].kwargs[key]

    def get_request(self):
        return self.context['request']

    @property
    def request(self):
        return self.get_request()


class CommentSerializer(RequestMixin, serializers.ModelSerializer):
    message = serializers.CharField(required=True)
    comment_url = serializers.SerializerMethodField()

    @permalink
    def get_comment_url(self, comment):
        return 'api_reply', [], {'pk': comment.pk}

    def create(self, validated_data):
        validated_data.update(
            object_pk=self.get_context_kwargs('object_pk'),
            content_type_id=self.get_context_kwargs('content_type'),
        )
        return get_model().objects.create(**validated_data)

    class Meta(object):
        model = get_model()
        exclude = ['content_type', 'object_pk', 'is_active', 'user',
                   'is_spam', 'is_moderated', 'remote_addr']


class CommentReplySerializer(RequestMixin, serializers.ModelSerializer):
    message = serializers.CharField(required=True)
    comment_url = serializers.SerializerMethodField()

    @permalink
    def get_comment_url(self, comment):
        return 'api_reply', [], {'pk': comment.pk}

    def create(self, validated_data):
        parent = get_model().objects.get(pk=self.get_context_kwargs('pk'))
        validated_data.update(
            content_object=parent.content_object,
            parent=parent
        )
        return get_model().objects.create(**validated_data)

    class Meta(CommentSerializer.Meta):
        pass


class LastReadSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = LastRead
