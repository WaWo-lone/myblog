# -*- author:caoyue -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^post-comment/(?P<article_id>\d+)/$', views.post_comment, name='post_comment'),
    url(r'^post-comment/(\d+)/(\d+)/', views.post_comment, name='post_comment'),
]