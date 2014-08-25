# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import template
from classytags.core import Tag, Options
from classytags.arguments import Argument, KeywordArgument
from classytags.helpers import InclusionTag


register = template.Library()


class InsertThreadedComments(InclusionTag):
    name = 'insert_comments'
    template = 'django_comments_threaded/templatetags/insert_comments.html'

    options = Options(
        'for',
        Argument('name', required=False, default='world'),
        'with',
        KeywordArgument('anonymous', required=False, default=True),
        KeywordArgument('template_name', required=False, default=None)

    )

    def get_template(self, context, **kwargs):
        return kwargs.get('template_name') or self.template

    def get_context(self, context, **kwargs):
        print('kwargs =', kwargs)
        return {'varname': 'dummy'}

#    def render_tag(self, context, name, varname):
#        output = 'hello %s' % name
#        if varname:
#            context[varname] = output
#            return ''
#        return output
#


register.tag(InsertThreadedComments)