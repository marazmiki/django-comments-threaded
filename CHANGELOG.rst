=========
CHANGELOG
=========

1.0.0
-----

* Now **django-comments-threaded** is standalone application, not **django-comments** example plugin
* Supported *both* **2.x** and **3.x** Python version
* Added documentation
* Added Django **1.7** and **1.8** support
* Added `Travis CI <https://travis-ci.org>`_ support
* Added `tox <https://testrun.org/tox/latest/>`_ support
* Added view to fetch unread comments (e.g. "update comments" feature)
* Added RESTful API (powered by `django rest framework <http://www.django-rest-framework.org/>`_)
* Time of last read comment now don't save automatically in favor of client side tracking
* Dropped Django 1.6x and older versions support
* Increase test coverage
* Full pep8 compatible
* Update dependencies
* Update client side libraries (`jQuery <https://jquery.com>`_ to 2.x, `Bootstrap <https://getbootstrap.com>`_ to 3.4x)
* Drop embedded jquery and bootstrap in favor of CDN
* Templates are prettified
