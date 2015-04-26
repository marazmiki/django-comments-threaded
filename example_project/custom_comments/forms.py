# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import forms
from django.utils.translation import ugettext_lazy as _
from django_comments_threaded import forms as dct


class Ng(object):
    namespace = 'newComment'

    def __init__(self, *args, **kwargs):
        super(Ng, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.required:
                field.widget.attrs['required'] = 'required'
            field.widget.attrs['ng-model'] = '{namespace}.{name}'.format(
                namespace=self.namespace,
                name=name,
            )

class CommentCreateForm(Ng, dct.CommentCreateForm):
    class Meta(dct.CommentCreateForm.Meta):
        widgets = dct.CommentCreateForm.Meta.widgets
        widgets.update(
            message=forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('Enter the comment'),
                'rows': 3,
            }),
            user_name=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Your name'),
            }),
            user_email=forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('Your e-mail'),
            }),
        )


class AnonymousCommentCreateForm(dct.AnonymousCommentCreateForm):
    pass
