# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.db import models, migrations
from django.conf import settings
from django.utils.timezone import now
import mptt.fields


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
            ],
            options={},
            bases=(models.Model,),
        ),

        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('lft', models.PositiveIntegerField(editable=False,
                                                    db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False,
                                                     db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False,
                                                        db_index=True)),
                ('level', models.PositiveIntegerField(editable=False,
                                                      db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, to='self',
                                                      null=True)),
                ('object_pk', models.CharField(default='', max_length=255,
                                               verbose_name='object ID')),
                ('content_type', models.ForeignKey(verbose_name='content type',
                                                   to='contenttypes.'
                                                      'ContentType')),
                ('message', models.TextField(verbose_name='message',
                                             default='')),
                ('date_created', models.DateTimeField(default=now,
                                                      verbose_name='Created',
                                                      editable=False)),
                ('user', models.ForeignKey(verbose_name='user', blank=True,
                                           to=settings.AUTH_USER_MODEL,
                                           null=True)),
                ('user_name', models.CharField(default='', max_length=255,
                                               verbose_name='user name')),
                ('user_email', models.EmailField(default='', max_length=255,
                                                 verbose_name='e-mail')),
                ('is_active', models.BooleanField(default=True, db_index=True,
                                                  blank=True,
                                                  verbose_name='Active')),
                ('is_moderated', models.BooleanField(
                    default=True, blank=True,
                    verbose_name='moderated')),
                ('is_spam', models.BooleanField(default=False, blank=True,
                                                verbose_name='moderated')),
                ('remote_addr', models.GenericIPAddressField(
                    null=True,
                    blank=True,
                    verbose_name='Remote ADDR')),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
                'index_together': [('content_type', 'object_pk')],
                'verbose_name': 'comment',
                'verbose_name_plural':  'comments',
            },
            bases=(models.Model,),
        ),

        migrations.CreateModel(
            name='LastRead',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('object_pk', models.CharField(default='', max_length=255,
                                               verbose_name='object ID')),
                ('content_type', models.ForeignKey(
                    verbose_name='content type',
                    to='contenttypes.ContentType')),
                ('user', models.ForeignKey(verbose_name='user', blank=True,
                                           to=settings.AUTH_USER_MODEL,
                                           null=True)),
                ('date_created', models.DateTimeField(default=now,
                                                      verbose_name='Created',
                                                      editable=False)),
                ('date_read', models.DateTimeField(
                    default=now,
                    verbose_name='Last read time')),
            ],
            options={
                'unique_together': [('content_type', 'object_pk', 'user')],
                'app_label': 'django_comments_threaded',
            },
            bases=(models.Model,),
        ),
    ]
