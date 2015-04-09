========================
django-comments-threaded
========================


.. image:: https://badge.fury.io/py/django-comments-thread.png
    :target: http://badge.fury.io/py/django-comments-thread
    :alt:

.. image:: https://travis-ci.org/marazmiki/django-comments-thread.png?branch=master
    :target: https://travis-ci.org/marazmiki/django-comments-thread
    :alt: Travis CI build status

.. image:: https://coveralls.io/repos/marazmiki/django-comments-thread/badge.png?branch=master
    :target: https://coveralls.io/r/marazmiki/django-comments-thread?branch=master
    :alt: Code coverage percentage

.. image:: https://pypip.in/d/django-comments-thread/badge.png
    :target: https://pypi.python.org/pypi/django-comments-thread
    :alt: Latest version on PyPI

.. image:: https://pypip.in/wheel/django-comments-thread/badge.svg
    :target: https://pypi.python.org/pypi/django-comments-thread/
    :alt: Wheel Status

.. image:: https://pypip.in/py_versions/django-comments-thread/badge.png
    :target: https://pypi.python.org/pypi/django-comments-thread/
    :alt: Supported Python versions


Requirements
------------

* Django 1.5 or higher;
* The `django-mptt <https://pypi.python.org/pypi/django-mptt>`_ 0.7
* The `django-generic-helpers <https://pypi.python.org/pypi/django-generic-helpers>`_ 0.4.2
* `django-classy-tags <https://pypi.python.org/pypi/django-classy-tags>`_

Installation
------------

Install package with pip (or easy_install) from `PyPI <https://pypi.python.org>`_:

.. code:: bash

    $ pip install django-comments-threaded

or development version from `github <https://github.com/marazmiki/django-comments-threaded>`_:

.. code:: bash

    $ pip install -e git+https://github.com/marazmiki/django-comments-threaded#egg=django-comments-threaded

Then you need add both **mptt** and **django_comments_threaded** applications into your **INSTALLED_APPS**:

.. code:: python

    # settings.py
    INSTALLED_APPS += (
        'mptt',
        'django_comments_threaded',
    )

and add URL schema to your project urlpatterns in **urls.py**:


.. code:: python

    # urls.py
    urlpatterns += [
        url(r'^comments/', include('django_comments_threaded.urls')),
    ]

After this run migrations:

.. code:: bash

    $ ./manage.py migrate

Usage
-----

A

.. code:: django

    {# some_template.html #}

    {% load comments_threaded_tags %}
    {% render_comments_widget for model_object %}


In this case **model_object** is the variable taken from template context that refers to instance of model
