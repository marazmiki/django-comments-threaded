# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.utils.timezone import now
from rest_framework import permissions


class CanDeleteOwnComment(permissions.BasePermission):
    TIMEOUT = 600

    def has_object_permission(self, request, view, obj):
        if request.method != 'DELETE':
            return True

        if self.grant_access(request.user):
            return True

        if self.is_own_object(obj, request.user):
            if self.no_replies(obj) and self.recently(obj):
                return True

        return False

    def grant_access(self, user):
        return user.is_superuser   # has_perm('delete_comment')?

    def is_own_object(self, obj, user):
        return obj.user == user

    def no_replies(self, obj):
        return not obj.has_replies()

    def recently(self, obj):
        return self.TIMEOUT >= (now() - obj.date_created).seconds
