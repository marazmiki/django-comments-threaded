# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.timezone import now
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt
from django_comments.views import CreateView as CreateViewBase
from django_comments_threaded.models import LastRead
from django_comments_threaded.forms import LoadNewCommentsForm
from django_comments_threaded.utils import get_last_read, now


class UpdateCommentsView(FormView):
    form_class = LoadNewCommentsForm
    comment_template_name = 'django_comments_threaded/item.html'

    def form_valid(self, form):
        last_read = now()
        queryset = []

        if self.request.is_authenticated():
            content_object = form.get_content_object()
            user = self.request.user

            last_read = get_last_read(content_object=content_object, user=user)
            queryset = self.plugin.get_queryset(request, content_object)
            queryset = queryset.filter(date_created__gt=last_read)

        return JsonResponse({
            'last_readed': last_read.replace(microsecond=0).isoformat(),
            'new_comments': [self.get_row(c) for c in queryset],
        })

    def get_row(self, comment):
        return {
            'html': self.render_comment(comment),
            'parent': comment.parent_comment_id,
            'id': comment.pk,
            'tree_id': comment.tree_id
        }

    def render_comment(self, comment):
        context_data = {
            'comment': comment,
        }

        return loader.render_to_string(
            self.comment_template_name,
            context_data,
            context_instance=RequestContext(self.request)
