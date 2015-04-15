#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
from django.conf import settings
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


settings.configure(
    ROOT_URLCONF='django_comments_threaded.tests',
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'mptt',
        'rest_framework',
        'django_comments_threaded',
        'django_comments_threaded.api',
    ),
    MIDDLEWARE_CLASSES=(
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ),
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':MEMORY:'
        }
    })


def main():
    from django.test.utils import get_runner
    import django

    if hasattr(django, 'setup'):
        django.setup()

    test_runner = get_runner(settings)(
        verbosity=3,
        interactive=True,
        failfast=True
    )

    failed = test_runner.run_tests([
        'django_comments_threaded.tests',
        'django_comments_threaded.api.tests',
    ])
    sys.exit(failed)


if __name__ == '__main__':
    main()
