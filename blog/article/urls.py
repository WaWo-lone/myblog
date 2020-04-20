# -*- author:caoyue -*-
from django.conf.urls import url

from article import views

urlpatterns = [
    # 首页
    url(r'^index/$', views.index, name='index'),

    # 个人文章列表
    url(r'^article_list/$', views.article_list, name='article_list'),

    # 文章详情
    url(r'^article_detail/(?P<pk>\d+)/$', views.article_detail, name='article_detail'),

    # 添加文章
    url(r'^article_add/$', views.article_add, name='article_add'),

    # 删除文章
    url(r'^article_delete/(?P<pk>\d+)/$', views.article_delete, name='article_delete'),

    # 修改文章
    url(r'^article_update/(?P<pk>\d+)/$', views.article_update, name='article_update'),

    # url(r'test/$', views.test, name='test')


]