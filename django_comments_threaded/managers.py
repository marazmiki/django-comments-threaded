# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from mptt.managers import TreeManager
from generic_helpers.managers import GenericQuerySet


class CommentQuerySet(GenericQuerySet, TreeManager):
    def public(self):
        return self.filter(is_spam=False, is_moderated=True)

    def spam(self):
        return self.filter(is_spam=True)

    def in_moderation(self):
        return self.filter(is_moderated=False)
