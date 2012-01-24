django-comments-threaded
========================

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

