# -*- coding: utf-8 -*-

from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.core.exceptions import PermissionDenied
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.decorators import method_decorator
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt

from django_comments.views import CreateView as CreateViewBase
from django_comments_threaded.utils import json_response
from django_comments_threaded.models import LastReaded
import datetime


class AjaxMixin(object):
    def render_to_string(self, request, template, context):
        """
        Renders the template and returns generated HTML code as string
        """
        return loader.render_to_string(
            self.get_templates_list(request, template), context,
            context_instance=RequestContext(request)
        )

    def get_templates_list(self, request, template):
        """
        Generates template search list that will be rendered
        """
        model = self.get_content_object(request)
        data = {
            'master'      : 'django_comments_threaded', # @TODO: make constant with this value to avoid a code duplicates?
            'template'    : template,
            'module_name' : model._meta.module_name,
            'app_label'   : model._meta.app_label,
            }
        return [
            '{master}/{app_label}/{module_name}/{template}.html'.format(**data),
            '{master}/{app_label}/{template}.html'.format(**data),
            '{master}/{template}.html'.format(**data),
            ]
class CreateView(CreateViewBase, AjaxMixin):
    """
    """
    parent_comment = None

    def get_content_object(self, request, kwargs={}):
        """
        Returns a model instance that will be a 'content object' for
        comment.
        """
        if hasattr(self, '_cached_content_object'):
            return self._cached_content_object

        # Returns the content object of parent comment if this is reply
        if 'pk' in self.kwargs:
            self.parent_comment = get_object_or_404(
                klass = self.plugin.get_model(request),
                pk    = self.kwargs['pk'],
            )
            self._cached_content_object = self.parent_comment.content_object  
            return self._cached_content_object 

        # Or retrieve content object data from POST 
        if request.method == 'POST':
            post = request.POST.get
            ctype = get_object_or_404(ContentType, pk=post('content_type'))
            self._cached_content_object = get_object_or_404(
                klass = ctype.model_class(), 
                pk    = post('object_pk'),
            )
            return self._cached_content_object

        # Or throws 404 error otherwise
        raise Http404, 'Failed to fetch content object: wrong method or params'

    def before_save(self, request, form, comment, kwargs={}):
        """
        Handles case before comment save if form filled correctly
        """
        comment.user          = request.user
        comment.remote_addr   = request.META.get('REMOTE_ADDR')
        comment.forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        comment.parent        = self.parent_comment

        if self.parent_comment:
            comment.insert_at(self.parent_comment,
                              position='last-child',
                              save=False)
        # If `on_success_before_save` returns a HttpResponse instance, view
        # function pass this response and not saves the comment.
        # We'll use this feature for "preview" implementation.
        if '_preview' in request.POST:
            return HttpResponse('Preview') # @TODO: make normal response for preview

    def after_save(self, request, form, comment, kwargs={}):
        """
        Handles case after comment save if form filled correctly.
        """
        obj = getattr(comment, self.plugin.content_object_field)

        if request.is_ajax():
            return json_response({
                'success': True,
                'parent_id': getattr(self.parent_comment, 'pk', None),
                'tree_id': comment.tree_id,
                'id': comment.pk,
                'comment': self.render_to_string(request, 'item', {
                    'comment': comment, 
                    'kwargs': kwargs
                }),
            })
        return redirect(obj)

    def failure(self, request, form, object, kwargs={}):
        """
        Handles case if form is incorrect.
        """
        if request.is_ajax():
            return json_response({
                'errors': dict([(k, unicode(v)) for k,v in form.errors.items()]),
                'success': False,
                'kwargs': kwargs
            })

        return self.render(request, 'failure', {
            'parent_comment': self.parent_comment,
            'form': form,
            'content_object': object,
            'kwargs': kwargs,
        })

    def get(self, request, *args, **kwargs):
        """
        Handles GET request
        """
        if 'pk' in self.kwargs:
            return self.render(request, 'reply', {
                'form': self.plugin.get_form(request, self.kwargs)(),
                'content_object': object,
                'kwargs': self.kwargs,
                'parent_comment': self.parent_comment
            })

        return HttpResponseNotAllowed('GET request allowed only in replying') 

    #### Plugin specific methods ####

    def render(self, request, template, context):
        """
        Renders the template and return HttpResponse object
        """
        return render(request, self.get_templates_list(request, template), 
                      context)


class UpdateCommentsView(CreateViewBase, AjaxMixin):
    def get_content_object(self, request, kwargs={}):
        """
        Returns a model instance that will be a 'content object' for
        comment.
        """
        model  = get_object_or_404(ContentType, pk=self.kwargs['content_type']).model_class()
        object = get_object_or_404(model,       pk=self.kwargs['object_pk'])
        return object

    def get(self, request, *args, **kwargs):
        return self.post(request, *args,**kwargs)
        return HttpResponseNotAllowed(['post'])

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        # @TODO: check?
        #if not request.is_ajax():
        #    return HttpResponse('XMLHttpRequest required', status=400)

        if not request.user.is_authenticated():
            return HttpResponse('Only for authenticated users', status=403)

        object = self.get_content_object(request, self.kwargs)

        # Log reading comments for given object by current user.
        readed, created = LastReaded.objects.get_or_create(
            content_object = object,
            user = request.user,
        )

        last_readed = readed.date_readed

        if not created:
            readed.date_readed = datetime.datetime.now()
            readed.save()

        # Gets comments that was written after current user last time  
        # has read comments to given object
        queryset = self.plugin.get_queryset(request, object)
        queryset = queryset.filter(date_created__gt=last_readed)

        return json_response({
            'last_readed': unicode(last_readed),
            'new_comments': [{
                'html': self.render_to_string(request, 'item', {'comment':c}),
                'parent': c.parent_comment_id,
                'id': c.pk,
                'tree_id': c.tree_id,
            } for c in queryset],
        })