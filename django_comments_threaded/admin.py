# coding: utf-8

from django.contrib import admin
from django_comments_threaded.models import Comment, LastReaded
from mptt.admin import MPTTModelAdmin


class CommentAdmin(MPTTModelAdmin):
    list_display = ['is_active', '__unicode__', 'is_spam', 'remote_addr', 'forwarded_for']
    raw_id_fields = ['user', 'parent_comment']


class LastReadedAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']


admin.site.register(Comment, CommentAdmin)
admin.site.register(LastReaded, LastReadedAdmin)