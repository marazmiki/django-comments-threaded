# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.core.exceptions import PermissionDenied
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.timezone import now
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt
from django_comments.views import CreateView as CreateViewBase
from django_comments_threaded.utils import json_response
from django_comments_threaded.models import LastRead
from django_comments_threaded.forms import LoadNewCommentsForm
from django_comments_threaded.utils import get_last_read, now


class UpdateCommentsView(FormView):
    form_class = LoadNewCommentsForm

    def form_valid(self, form):
        last_read = now()
        queryset = []

        if self.request.is_authenticated():
            content_object = form.get_content_object()
            user = self.request.user

            last_read = get_last_read(content_object=content_object, user=user)
            queryset = self.plugin.get_queryset(request, content_object)
            queryset = queryset.filter(date_created__gt=last_read)

        return json_response({
            'last_readed': last_read.replace(microsecond=0).isoformat(),
            'new_comments': [{
                'html': self.render_to_string(request, 'item', {'comment': c}),
                'parent': c.parent_comment_id,
                'id': c.pk,
                'tree_id': c.tree_id,
            } for c in queryset],
        })