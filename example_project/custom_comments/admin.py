# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.contrib import admin
from custom_comments.models import CustomComment


admin.site.register(CustomComment)
