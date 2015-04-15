#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
import os


def read_file(filename):
    try:
        with open(os.path.join(CWD, filename)) as fp:
            return fp.read()
    except (OSError, IOError):
        return ''


def get_long_description():
    return "{README}\n\n{CHANGELOG}".format(
        README=read_file('README.rst'),
        CHANGELOG=read_file('CHANGELOG.rst')
    )


CWD = os.path.dirname(__file__)
VERSION = __import__('django_comments_threaded').get_version()
REQUIREMENTS = [
    'Django>=1.7',
    'django-mptt',
    'django-generic-helpers',
]
CLASSIFIERS = [
    'Operating System :: OS Independent',
    'Environment :: Web Environment',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Framework :: Django'
]

setup(name='django-comments-threaded',
      author='Mikhail Porokhovnichenko',
      version=VERSION,
      author_email='marazmiki@gmail.com',
      description='An application that implements threaded comments',
      long_description=get_long_description(),
      license='MIT license',
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      packages=find_packages(exclude=['example_project', 'example_project.*']),
      test_suite='tests.main',
      include_package_data=True,
      zip_safe=False)
