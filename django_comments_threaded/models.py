# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from generic_helpers.models import GenericRelationModel
import mptt

class Comment(GenericRelationModel):
    """
    Habrahabr like threaded comment model
    """
    ct_related_name = 'djc_%(class)s_set'

    message = models.TextField(
        verbose_name = _('Message'),
        default = '',
    )
    user = models.ForeignKey(User,
        verbose_name = _('User'),
        related_name = 'comments',
    )
    parent_comment = models.ForeignKey('self',
        verbose_name = _('Parent'),    
        related_name = 'children',
        blank = True,
        null  = True,
    )
    date_created = models.DateTimeField(
        verbose_name = _('Created'),
        blank   = True,
        default = datetime.now,
    )
    is_active = models.BooleanField(
        verbose_name = _('Active'),
        db_index = True,
        default  = True, 
    )
    is_spam = models.BooleanField(
        verbose_name = _('Marked as spam'),
        db_index = True,
        default  = False, 
    )
    remote_addr = models.IPAddressField(
        verbose_name = _('Remote ADDR'),
        blank = True,
        null = True,
    )
    forwarded_for = models.IPAddressField(
        verbose_name = _('Forwarded for'),
        blank = True,
        null = True,
    )

    def __unicode__(self):
        return self.message[:30]

    @models.permalink
    def get_reply_url(self):
        return 'threaded_comments_reply', [self.pk]

    class Meta:
        db_table = 'comments_threaded'
        ordering = ['tree_id', 'lft']
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


class LastReaded(GenericRelationModel):
    """
    Model for storing last comment reading date and time by user. 
    """
    user = models.ForeignKey(User,
        verbose_name = _('User'),
        related_name = 'last_readed',
    )
    date_created = models.DateTimeField(
        verbose_name = _('Created'),
        blank   = True,
        default = datetime.now,
    )
    date_readed = models.DateTimeField(
        verbose_name = _('Last reading'),
        blank   = True,
        default = datetime.now,
    )

    def __unicode__(self):
        return unicode(_('User {user} has read "{what}" at {date}')).format(
            user = self.user,
            what = self.content_object,
            date = self.date_readed,
        )

    class Meta:
        unique_together = [('content_type', 'object_pk', 'user')]
        db_table = 'threaded_comments_readed'


mptt.register(Comment, 
        parent_attr = 'parent_comment',
        order_insertion_by = ['date_created'])
