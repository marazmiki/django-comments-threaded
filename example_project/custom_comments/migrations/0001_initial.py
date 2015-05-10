# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import mptt.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_pk', models.CharField(default='', max_length=255, verbose_name='object ID')),
                ('message', models.TextField(default='', verbose_name='message')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created', editable=False)),
                ('user_name', models.CharField(default='', max_length=255, verbose_name='user name')),
                ('user_email', models.EmailField(default='', max_length=255, verbose_name='e-mail')),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='Active')),
                ('is_moderated', models.BooleanField(default=True, verbose_name='moderated')),
                ('is_spam', models.BooleanField(default=False, db_index=True, verbose_name='Marked as spam')),
                ('remote_addr', models.GenericIPAddressField(null=True, verbose_name='Remote ADDR', blank=True)),
                ('website', models.URLField(verbose_name='Site')),
                ('device', models.CharField(default='desktop', max_length=25, verbose_name='device', choices=[('desktop', 'desktop'), ('android', 'android'), ('mobile', 'mobile'), ('apple', 'apple')])),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('thread_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('content_type', models.ForeignKey(related_name='ct_set_for_customcomment', verbose_name='content type', to='contenttypes.ContentType')),
                ('parent', mptt.fields.TreeForeignKey(related_name='replies', verbose_name='parent', blank=True, to='custom_comments.CustomComment', null=True)),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['thread_id', 'lft'],
                'abstract': False,
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
            },
        ),
        migrations.AlterIndexTogether(
            name='customcomment',
            index_together=set([('content_type', 'object_pk')]),
        ),
    ]
