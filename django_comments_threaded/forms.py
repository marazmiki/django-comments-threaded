# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import forms
from django_comments_threaded.models import Comment


class CommentForm(forms.ModelForm):
    class Meta(object):
        model = Comment
        fields = ['message', 'content_type', 'object_pk']
        widgets = {'content_type': forms.HiddenInput(),
                   'object_pk': forms.HiddenInput()
                   }


class CommentReplyForm(forms.ModelForm):
    class Meta(object):
        model = Comment
        fields = ['message']


class AnonymousCommentForm(CommentForm):
    class Meta(CommentForm.Meta):
        fields = ['user_name', 'user_email'] + CommentForm.Meta.fields


class AnonymousReplyForm(CommentReplyForm):
    class Meta(CommentReplyForm.Meta):
        fields = ['user_name', 'user_email'] + CommentReplyForm.Meta.fields