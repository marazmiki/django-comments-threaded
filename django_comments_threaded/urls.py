# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django_comments import codename
from django_comments.urls import URLConf


urlpatterns = URLConf(codename).get_urls()
