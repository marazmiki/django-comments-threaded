# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import forms
from django_comments_threaded.models import Comment


class CommentCreateForm(forms.ModelForm):
    class Meta(object):
        model = Comment
        exclude = []

#
# class LoadNewCommentsForm(forms.Form):
#     object_pk = forms.CharField(widget=forms.HiddenInput())
#     content_type = forms.ModelChoiceField(queryset=ContentType.objects.all(),
#                                           widget=forms.HiddenInput())
#
#     def get_content_object(self):
#         assert self.is_valid(), "This method can be called " \
#                                 "only for valid models"
#         content_type = self.cleaned_data['content_type']
#         object_pk = self.cleaned_data['object_pk']
#         return content_type.get_object_for_this_type(pk=object_pk)
#
#
# class CommentForm(forms.ModelForm):
#     class Meta(object):
#         model = Comment
#         fields = ['message', 'content_type', 'object_pk']
#         widgets = {'content_type': forms.HiddenInput(),
#                    'object_pk': forms.HiddenInput()
#                    }
#
#
# class CommentReplyForm(forms.ModelForm):
#     class Meta(object):
#         model = Comment
#         fields = ['message']
#
#
# class AnonymousCommentForm(CommentForm):
#     class Meta(CommentForm.Meta):
#         fields = ['user_name', 'user_email'] + CommentForm.Meta.fields
#
#
# class AnonymousReplyForm(CommentReplyForm):
#     class Meta(CommentReplyForm.Meta):
#         fields = ['user_name', 'user_email'] + CommentReplyForm.Meta.fields
