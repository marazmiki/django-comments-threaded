# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django_comments_threaded.models import Comment

class CommentForm(forms.ModelForm):
    """
    Form for creation habrahabr like comments
    """
    class Meta:
        model   = Comment
        fields  = ['message', 'content_type', 'object_pk']
        widgets = {
            'content_type': forms.HiddenInput(),
            'object_pk':    forms.HiddenInput(),
        }

class CommentReplyForm(forms.ModelForm):
    """
    Form for replying habrahabr like comments
    """
    class Meta:
        model   = Comment
        fields  = ['message']
