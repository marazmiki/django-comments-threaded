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

* Django 1.3 or higher
* The `django-mptt` package of 0.4.2 version
* The `django-generic-helpers` package

Installation
------------

* Install the package from github (currently there is no this package in PyPI)
* Add `django_comments`, `django_comments_threaded`, and `mptt` apps into your INSTALLED_APPS (`settings.py`)
* Add the string `COMMENTS_PLUGINS = ('django_comments_threaded.plugins.ThreadedCommentPlugin',)` into your `settings.py`
* Run `./manage.py syncdb` (currently there are no South migrations inside)
* Run `./manage.py collectstatic` to collect JS
* Add the `url('^comments/', include('django_comments_threaded.urls'))` pattern into your URLconf (`urls.py`)

Usage
-----

Basic example:

::
    {# some_template.html #}

    {% load comments_threaded_tags %}
    {% render_comments_widget for model_object %}


In this case `model_object` is the variable taken from template context that refers to 
instance of model
