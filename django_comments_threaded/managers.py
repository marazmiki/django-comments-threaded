# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.db.models import QuerySet
from mptt.managers import TreeManager


class CommentQuerySet(QuerySet, TreeManager):
    def spam(self):
        return self.filter(is_spam=True)

    def in_moderation(self):
        return self.filter(is_moderated=False)
