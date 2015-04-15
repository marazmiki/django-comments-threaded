# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.utils.module_loading import import_by_path
from django.conf import settings


__all__ = ['get_create_form', 'get_reply_form', 'get_model']


def get_create_form():
    """
    Returns the new comment form class.

    If the default `CommentCreateForm` does not satisfy your requirements,
    you can specify own form with override `THREADED_COMMENTS_CREATE_FORM`
    attribute in your `settings.py`:

        THREADED_COMMENTS_CREATE_FORM = 'my_app.forms.MyCreateForm'

    Path to model call must be full cause `import_by_path` Django
    utility is used.

    :return: forms.ModelForm
    """
    return _ex('THREADED_COMMENTS_CREATE_FORM',
               'django_comments_threaded.forms.CommentCreateForm')


def get_reply_form():
    """
    Returns the reply comment form class.

    If the default `CommentReplyForm` does not satisfy your requirements,
    you can specify own form with override `THREADED_COMMENTS_REPLY_FORM`
    attribute in your `settings.py`:

        THREADED_COMMENTS_REPLY_FORM = 'my_app.forms.MyReplyForm'

    Path to model call must be full cause `import_by_path` Django
    utility is used.

    :return: forms.ModelForm
    """
    return _ex('THREADED_COMMENTS_REPLY_FORM',
               'django_comments_threaded.forms.CommentReplyForm')


def get_model():
    """
    Returns the comment model class.

    If the default `Comment` model does not satisfy your requirements,
    you can specify own custom model with override `THREADED_COMMENTS_MODEL`
    attribute in your `settings.py`:

        THREADED_COMMENTS_MODEL = 'my_app.models.MyCommentModel'

    Path to model call must be full cause `import_by_path` Django
    utility is used.

    **IMPORTANT**: if you want use custom comment model, highly recommended
    inherit its class from `django_comments_threaded.models.AbstractComment`
    one

    :return: Comment
    """
    return _ex('THREADED_COMMENTS_MODEL',
               'django_comments_threaded.models.Comment')


def _ex(name, default):
    """
    Returns callable object based on `name` or `default`
    Raises ImportError if can't import given name.

    :param name: str
    :param default: str
    :return: callable
    """
    return import_by_path(getattr(settings, name, default))
