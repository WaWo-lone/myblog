# -*- author:caoyue -*-
import logging

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from common.func import check_token
from user.models import BlogUser


class AuthMiddleware(MiddlewareMixin):

    # 设置白名单，把不需要进行登录验证的地址放入
    # WHITE_LIST = ['/user/register/', '/user/sms/', '/user/logout/']

    def process_request(self, request):

        # url = request.path
        # if url in self.WHITE_LIST:
        #     # 默认返回None，会继续执行
        #     return

        if request.session.get('id'):
            uid = request.session.get('id')
            request.users = BlogUser.objects.get(id=uid)
        else:
            request.users = ''
        # # 获取token
        # token = request.META.get('HTTP_AUTHORIZATION')
        #
        # if token:
        #     # 验证token是否正确
        #     flag, uid = check_token(token)
        #
        #     if flag:
        #         # 验证成功
        #         # 将用户数据添加到request中
        #         request.users = BlogUser.objects.get(id=uid)
        #     else:
        #         return render(request, 'user/login.html', {'code': 1002, 'msg': '用户验证登录失败'})
        # else:
        #     return render(request, 'user/login.html', {'msg': ''})

    def request_exception(self, request, exception):
        inf_log = logging.getLogger('inf')
        inf_log.info(str(exception))