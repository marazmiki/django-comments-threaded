# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.db.models.manager import Manager
from django.contrib.contenttypes.models import ContentType
from mptt.managers import TreeManager
from mptt.querysets import TreeQuerySet


def ct(mdl_cls):
    """
    Shortcut for get_for_model method of ContentType manager
    """
    return ContentType.objects.get_for_model(mdl_cls)


class CommentQuerySet(TreeQuerySet):
    """
    """
    gr_field = 'content_object'
    ct_field = 'content_type'
    fk_field = 'object_pk' 

    def _filter_or_exclude(self, negate, *args, **kwargs):
        if self.gr_field in kwargs:
            instance = kwargs.pop(self.gr_field)
            kwargs.update(**{self.ct_field: ct(instance),
                             self.fk_field: instance.pk
                             })
        return super(CommentQuerySet, self)._filter_or_exclude(negate, *args,
                                                               **kwargs)

    def get_for_object(self, content_object):
        return self.filter(**{self.gr_field: content_object})

    def get_for_model(self, model):
        return self.filter(**{self.gr_field: ct(model)})

    def public(self):
        return self.filter(is_spam=False, is_moderated=True, is_active=True)

    def spam(self):
        return self.filter(is_spam=True)

    def in_moderation(self):
        return self.filter(is_moderated=False)


class CommentManager(TreeManager):
    gr_field = 'content_object'
    ct_field = 'content_type'
    fk_field = 'object_pk'

    def get_queryset(self, *args, **kwargs):
        """
        Ensures that this manager always returns nodes in tree order.
        """
        return CommentQuerySet(self.model, using=self._db).order_by(
            self.tree_id_attr,
            self.left_attr
        )

    def get_for_object(self, content_object):
        return self.get_queryset().filter(**{self.gr_field: content_object})

    def get_for_model(self, model):
        return self.get_queryset().filter(**{self.gr_field: ct(model)})

    def public(self):
        return self.get_queryset().filter(is_spam=False, is_moderated=True,
                                          is_active=True)

    def spam(self):
        return self.filter(is_spam=True)

    def in_moderation(self):
        return self.filter(is_moderated=False)
