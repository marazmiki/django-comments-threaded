# coding: utf-8

from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils import six
from generic_helpers.models import GenericRelationModel
from mptt.models import MPTTModel
import mptt.fields


@python_2_unicode_compatible
class AbstractCommentBase(MPTTModel, GenericRelationModel):
    message = models.TextField(_('message'), default='')
    date_created = models.DateTimeField(_('Created'),
                                        default=now,
                                        editable=False)
    parent = mptt.fields.TreeForeignKey('self', related_name='childs',
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
                             verbose_name=_('user'))
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
    remote_addr = models.IPAddressField(_('Remote ADDR'),
                                        blank=True,
                                        null=True)
    forwarded_for = models.IPAddressField(_('Forwarded for'),
                                          blank=True,
                                          null=True)

    class Meta(object):
        abstract = True


class Comment(AbstractComment):
    class Meta(object):
        ordering = ['tree_id', 'lft']
        index_together = [('content_type', 'object_pk')]
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


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
        what = self.content_object
        return six.text_type(_('{user} has read {what}'.format(user=self.user,
                                                               what=what)))

    class Meta(object):
        unique_together = [('content_type', 'object_pk', 'user')]
        app_label = 'django_comments_threaded'
