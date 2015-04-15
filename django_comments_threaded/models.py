# coding: utf-8

from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils import six
from generic_helpers.models import GenericRelationModel
from django_comments_threaded.managers import CommentQuerySet
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey


@python_2_unicode_compatible
class AbstractCommentBase(MPTTModel, GenericRelationModel):
    message = models.TextField(_('message'), default='')
    date_created = models.DateTimeField(_('Created'), default=now,
                                        editable=False)
    parent = TreeForeignKey('self', related_name='childs',
                            verbose_name=_('parent'),
                            blank=True,
                            null=True)

    def __str__(self):
        return self.message[:30]

    @models.permalink
    def get_reply_url(self):
        return 'threaded_comments_reply', [self.pk]

    class MPTTMeta(object):
        parent_attr = 'parent'

    class Meta(object):
        abstract = True


class AbstractComment(AbstractCommentBase):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='comments',
                             verbose_name=_('user'), null=True)
    user_name = models.CharField(_('user name'), max_length=255,
                                 default='')
    user_email = models.EmailField(_('e-mail'), max_length=255,
                                   default='')
    is_active = models.BooleanField(_('Active'), db_index=True,
                                    default=True, blank=True)
    is_moderated = models.BooleanField(_('moderated'), blank=True,
                                       default=False)
    is_spam = models.BooleanField(_('Marked as spam'),
                                  db_index=True,
                                  default=False)
    remote_addr = models.GenericIPAddressField(_('Remote ADDR'),
                                               blank=True,
                                               null=True)
    objects = CommentQuerySet.as_manager()

    def soft_delete(self):
        self.is_active = False
        self.save(update_fields=['is_active'])

    def has_replies(self):
        return self.count_replies() > 0

    def count_replies(self):
        return int((self.rght - self.lft) / 2)

    class Meta(object):
        abstract = True
        ordering = ['tree_id', 'lft']
        index_together = [('content_type', 'object_pk')]
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


class Comment(AbstractComment):
    class Meta(AbstractComment.Meta):
        pass


@python_2_unicode_compatible
class LastRead(GenericRelationModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='last_read',
                             verbose_name=_('user'))
    date_created = models.DateTimeField(_('created'),
                                        editable=False,
                                        default=now)
    date_read = models.DateTimeField(_('Last read time'),
                                     default=now)

    def __str__(self):
        return six.text_type(_('{user} has read {what}')).format(
            user=self.user,
            what=self.content_object)

    class Meta(object):
        unique_together = [('content_type', 'object_pk', 'user')]
        app_label = 'django_comments_threaded'
