# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect
from django_comments_threaded.forms import CommentCreateForm


class CreateCommentView(CreateView):
    form_class = CommentCreateForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.save()
        return self.redirect_or_json()


class ReplyCommentView(UpdateView):
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.parent = self.get_object()
        comment.user = self.request.user


class LastReadView(object):
    pass


class MarkReadView(object):
    pass

#
# class UpdateCommentsView(FormView):
#     form_class = LoadNewCommentsForm
#     comment_template_name = 'django_comments_threaded/item.html'
#
#     def form_valid(self, form):
#         last_read = now()
#         queryset = []
#
#         if self.request.is_authenticated():
#             content_object = form.get_content_object()
#             user = self.request.user
#
#             last_read = get_last_read(content_object=content_object, user=user)
#             queryset = self.plugin.get_queryset(self.request, content_object)
#             queryset = queryset.filter(date_created__gt=last_read)
#
#         return JsonResponse({
#             'last_readed': last_read.replace(microsecond=0).isoformat(),
#             'new_comments': [self.get_row(c) for c in queryset],
#         })
#
#     def get_row(self, comment):
#         return {
#             'html': self.render_comment(comment),
#             'parent': comment.parent_comment_id,
#             'id': comment.pk,
#             'tree_id': comment.tree_id
#         }
#
#     def render_comment(self, comment):
#         context_data = {
#             'comment': comment,
#         }
#
#         return loader.render_to_string(
#             self.comment_template_name,
#             context_data,
#             context_instance=RequestContext(self.request)
#             )
