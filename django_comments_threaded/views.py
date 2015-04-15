# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django_comments_threaded.utils import get_create_form, get_reply_form
from django_comments_threaded.signals import comment_created, comment_replied


class CreateCommentView(CreateView):
    """
    Create new comment thread
    """
    form_class = get_create_form()
    template_name = 'django_comments_threaded/comment_create.html'

    def form_valid(self, form):
        comment = form.save(commit=False)

        if self.request.user.is_authenticated():
            comment.user = self.request.user

        comment.save()
        comment_created.send(sender=comment.__class__,
                             comment=comment,
                             request=self.request)

        if hasattr(comment.content_object, 'get_absolute_url'):
            return redirect(comment.content_object)

        return redirect('/')


class ReplyCommentView(CreateView):
    """
    Reply to existing comment (same thread)
    """
    form_class = get_reply_form()
    template_name = 'django_comments_threaded/comment_reply.html'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.parent = self.get_object()
        comment.user = self.request.user

        comment_replied.send(sender=comment.__class__,
                             comment=comment,
                             parent=comment.parent,
                             request=self.request)

        return redirect(comment.content_object)
