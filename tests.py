#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
from django.conf import settings
from django import get_version
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
app_name = 'django_comments_threaded'


settings.configure(
    DEBUG=True,
    ROOT_URLCONF='%s.tests.urls' % app_name,
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        app_name,
    ),
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':MEMORY:'
        }
    })


def main():
    from django.test.utils import get_runner

    find_pattern = app_name

    if get_version() >= '1.6':
        find_pattern += '.tests'

    test_runner = get_runner(settings)(verbosity=2, interactive=True)
    failed = test_runner.run_tests([find_pattern])

    sys.exit(failed)


if __name__ == '__main__':
    main()
