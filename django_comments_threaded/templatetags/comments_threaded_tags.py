# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType
from django import template
from django.core.urlresolvers import reverse
from django_comments.plugins import plugin_pool
from django_comments_threaded.models import LastReaded
from django_comments_threaded.utils import get_update_url
import datetime

class CommentNodeBase(template.Node):
    """
    Base comment node class
    """

class RenderCommentNodeBase(CommentNodeBase):
    """
    Base render comment node class
    """
    default_template = ''

    def __init__(self, object, tpl_name=None):
        """
        It takes two arguments: `object` (required) is a content object of
        type Model instance. Second one `tpl_name` (optional) picks for
        template will be rendered. If not specified, will be used default.
        """
        self.object = template.Variable(object)
        self.plugin = plugin_pool.get_plugin('threaded')
        self.template_name = template.Variable(tpl_name) if tpl_name else None

    def render(self, context):
        """
        Render node and outputs HTML
        """
        object = self.object.resolve(context)
        format = {
            'dir' : 'django_comments_threaded',
            'tpl' : self.default_template,  
            'app_label'   : object._meta.app_label,
            'module_name' : object._meta.module_name,
        }
        template_name = self.template_name.resolve(context) \
            if self.template_name else \
            [
                '{dir}/{app_label}/{module_name}/{tpl}.html'.format(**format),
                '{dir}/{app_label}/{tpl}.html'.format(**format),
                '{dir}/{tpl}.html'.format(**format),
            ]
        context['content_object'] = object
        context.update(self.get_extra_context(context['request'], context))

        return template.loader.render_to_string(template_name, context, 
            context_instance = template.RequestContext(context['request'])
        )

    def get_extra_context(self, request, context={}):
        """
        Puts new pairs into context dictonary
        """
        return {}


class RenderCommentsWidgetNode(RenderCommentNodeBase):
    """
    Whole comment widget renderer template tag class
    """
    default_template = 'widget'


class RenderCommentsListNode(RenderCommentNodeBase):
    """
    Comment list renderer template tag class
    """
    default_template = 'list'


class UpdateCommentsUrlNode(RenderCommentNodeBase):
    def render(self, context):
        """
        Render node and outputs HTML
        """
        return get_update_url( self.object.resolve(context) )

class RenderCommentsFormNode(RenderCommentNodeBase):
    """
    Comment form renderer template tag class
    """
    default_template = 'form'

    def get_extra_context(self, request, context={}):
        obj  = context['content_object']

        if False and context['content_object'].parent_comment_id:
            action = context['content_object'].get_reply_url()

        else:
            action = reverse('threaded_comments_create')

        return {
            'form': self.plugin.get_form(request)(initial={
                'object_pk': obj.pk,
                'content_type': ContentType.objects.get_for_model(obj),
            }),
            'action': action
        }


class GetCommentsListNode(CommentNodeBase):
    """
    Comments list tempalte tag class
    """
    def __init__(self, object, varname):
        """
        The class constructor
        """
        self.object  = template.Variable(object)
        self.varname = template.Variable(varname)
        self.plugin  = plugin_pool.get_plugin('threaded')

    def render(self, context):
        """
        Push comments list into template context
        """
        request = context['request']
        varname  = self.varname.resolve(context)
        object   = self.object.resolve(context)
        queryset = self.plugin.get_queryset(request, object)

        # Highlights the unreaded comments for authenticated user.  
        if request.user.is_authenticated():

            # Log reading comments for given object by current user.
            readed, created = LastReaded.objects.get_or_create(
                content_object = object,
                user     = request.user,
            )

            # Store the time when current user last time readed
            # comments for given object.
            last_readed = readed.date_readed

            if not created:
                readed.date_readed = datetime.datetime.now()
                readed.save()

            # Add attribute `new` for each comment that was written after
            # user last time readed comments.
            comments = []

            for c in queryset:
                if c.date_created > last_readed:
                    c.new = True
                comments.append(c) 
            queryset = comments

        context[varname] = queryset
        return ''


def _render(parser, token, cls):
    """
    Helper for generation render tags.

    First and second argument is `parser` and `token` corresponds with
    input argument for any template tag. Third argument `cls` is Node
    subclass that renders tag
    """
    bits = token.split_contents()
    args = [bits[2]]

    if len(bits) not in [3, 6]:
        raise template.TemplateSyntaxError, '%s: wrong number or args' % bits[0]

    if bits[1] != 'for':
        raise template.TemplateSyntaxError, '%s: first word must ' % bits[0]+ \
                                            'be `for`'
    if len(bits) == 6:
        if bits[3] != 'with' or bits[4] != 'template':
            raise template.TemplateSyntaxError, \
                '%s: after `content_object` variable must follow ' % bits[0] + \
                '`with template` statement'
        args.append(bits[5])

    return cls(*args)


def _update_context(parser, token, cls):
    """
    Helper for generation update template context tags.

    First and second argument is `parser` and `token` corresponds with
    input argument for any template tag. Third argument `cls` is Node
    subclass that changes template context

    {% TAGNAME for `object` as `varname` %}
    """
    bits = token.split_contents()

    if len(bits) != 5:
        raise template.TemplateSyntaxError, '%s: wrong number or args' % bits[0]

    if bits[1] != 'for':
        raise template.TemplateSyntaxError, '%s: first word must ' % bits[0]+ \
                                            'be `for`'
    if bits[3] != 'as':
        raise template.TemplateSyntaxError, '%s: third word must ' % bits[0]+ \
                                            'be `as`'
    return cls(bits[2], bits[4])


def render_comments_widget(parser, token):
    """
    {% render_comments_widget for `object` %}
    {% render_comments_widget for `object` with template `template_name` %}    
    """
    return _render(parser, token, RenderCommentsWidgetNode)


def render_comments_list(parser, token):
    """
    {% render_comments_list for `object` %}
    {% render_comments_list for `object` with template `template_name` %}    
    """
    return _render(parser, token, RenderCommentsListNode)


def render_comments_form(parser, token):
    """
    {% render_comments_form for `object` %}
    {% render_comments_form for `object` with template `template_name` %}    
    """
    return _render(parser, token, RenderCommentsFormNode)

def render_update_comments_url(parser, token):
    """
    {% render_update_comments_url for `object` %}
    {% render_update_comments_url for `object` with template `template_name` %}    
    """
    return _render(parser, token, UpdateCommentsUrlNode)

def get_comments_list(parser, token):
    """
    {% get_comments_list for `object` as `varname` %}    
    """
    return _update_context(parser, token, GetCommentsListNode)


register = template.Library()
register.tag(render_comments_widget)
register.tag(render_comments_list)
register.tag(render_comments_form)
register.tag(render_update_comments_url)
register.tag(get_comments_list)