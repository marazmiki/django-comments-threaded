#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
version = __import__('django_comments_threaded').get_version()

CLASSIFIERS=[
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Framework :: Django'
]

setup(
    name = 'django-comments-threaded',
    author = 'marazmiki',
    version = version,
    author_email = 'marazmiki@gmail.com',
    description = 'The threaded comments plugin for django-comments',
    long_description = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    license = 'MIT license',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=[
        'Django>=1.3',
        'django-mptt==0.4.2',
        'django-generic-helpers',
        'django-comments',
        ],
    packages=find_packages(exclude=['test_project', 'test_project.*']),
    include_package_data=True,
    zip_safe = False
)

