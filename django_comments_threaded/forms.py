# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import forms
from django_comments_threaded.utils import get_model


GR_EX = ['object_pk', 'content_type']
USER_EX = ['user_name', 'user_email']
COMMON_EX = ['is_active', 'parent', 'user', 'is_spam', 'is_moderated',
             'remote_addr']

WIDGETS = {
    'content_type': forms.HiddenInput(),
    'object_pk': forms.HiddenInput(),
}


class CommentCreateForm(forms.ModelForm):
    class Meta(object):
        model = get_model()
        exclude = COMMON_EX  # + USER_EX
        widgets = WIDGETS


class CommentReplyForm(forms.ModelForm):
    class Meta(object):
        model = get_model()
        exclude = COMMON_EX + GR_EX  # + USER_EX


class AnonymousCommentCreateForm(CommentCreateForm):
    class Meta(CommentCreateForm.Meta):
        exclude = COMMON_EX


class AnonymousCommentReplyForm(forms.ModelForm):
    class Meta(CommentReplyForm.Meta):
        exclude = COMMON_EX + GR_EX + USER_EX
