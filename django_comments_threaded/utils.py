# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.utils.timezone import now
from django_comments_threaded.models import LastRead


def get_last_read(content_object, user):
    read, created = LastRead.objects.get_or_create(
        content_object=content_object,
        user=user)

    read_time = read.date_read

    if not created:
        read.date_read = now()
        read.save(update_fields=['date_read'])

    return read_time