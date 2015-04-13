# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.contrib import admin
from django_comments_threaded.models import Comment, LastRead
from mptt.admin import MPTTModelAdmin


class CommentAdmin(MPTTModelAdmin):
    list_display = ['is_active', '__str__',
                    'is_spam', 'remote_addr', 'forwarded_for']
    raw_id_fields = ['user', 'parent']


class LastReadAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']


admin.site.register(Comment, CommentAdmin)
admin.site.register(LastRead, LastReadAdmin)
