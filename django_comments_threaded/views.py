# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django_comments_threaded.signals import comment_created, comment_replied
from django_comments_threaded.utils import (get_create_form, get_reply_form, 
                                            get_model)


class CommentMixin(object):
    def save_comment(self, comment):
        if self.request.user.is_authenticated():
            comment.user = self.request.user
        comment.save()

    def redirect(self, comment):
        if hasattr(comment.content_object, 'get_absolute_url'):
            return redirect(comment.content_object)
        return redirect('/')


class CreateCommentView(CommentMixin, CreateView):
    """
    Create new comment thread
    """
    form_class = get_create_form()
    template_name = 'django_comments_threaded/comment_create.html'

    def form_valid(self, form):
        comment = form.save(commit=False)

        self.save_comment(comment)

        comment_created.send(sender=comment.__class__,
                             comment=comment,
                             request=self.request)

        return self.redirect(comment)


class ReplyCommentView(CommentMixin, CreateView):
    """
    Reply to existing comment (same thread)
    """
    form_class = get_reply_form()
    template_name = 'django_comments_threaded/comment_reply.html'

    def get_queryset(self):
        return get_model().objects.public()

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.parent = self.get_object()
        comment.content_object = comment.parent.content_object

        self.save_comment(comment)

        comment_replied.send(sender=comment.__class__,
                             comment=comment,
                             parent=comment.parent,
                             request=self.request)
        return self.redirect(comment)
