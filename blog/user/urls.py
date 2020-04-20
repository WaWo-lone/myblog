# -*- author:caoyue -*-
from django.conf.urls import url

from user import views

urlpatterns = [

    # 注册
    url(r'^register/$', views.register, name='register'),
    # 验证码
    url(r'^sms/$', views.sms, name='sms'),
    # 登录
    url(r'^login/$', views.login_user, name='login'),
    # 登出
    url(r'^logout/$', views.logout_user, name='logout'),
    # 博客信息
    url(r'^mine/$', views.mine, name='mine'),
    # 修改博客信息
    url(r'^edit/$', views.edit, name='edit')

]