# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.views.generic import ListView, DetailView, TemplateView
from posts.models import Post, Link


class PostListView(ListView):
    model = Post


class PostDetailView(DetailView):
    model = Post


class LinkListView(ListView):
    model = Link


class LinkDetailView(DetailView):
    model = Link


class IndexView(TemplateView):
    template_name = 'posts/index.html'
