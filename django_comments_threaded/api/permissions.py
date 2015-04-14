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

        return (
            request.user == obj.user and
            now() - obj.date_created).seconds < TIMEOUT and
            not obj.has_replies()
        )
        return request.user.is_superuser  # has_perm('delete_comment')

