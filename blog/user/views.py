import os

from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from common.func import sendSms, create_token, auth
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from .models import BlogUser
from django_redis import get_redis_connection
import re
from blog.settings import BASE_DIR



def register(request):
    if request.method == 'GET':
        return render(request, 'user/register.html', {'msg': ''})
    if request.method == 'POST':
        # 获取数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        avatar = request.FILES.get('avatar')
        phone = request.POST.get('phone')
        smscode = request.POST.get('smscode')

        # 2，判断参数
        # 2.0 判断所有字段不能为空格
        if not all([username, password, password2, avatar, phone, smscode]):
            return render(request, 'user/register.html', {'msg': '选项不能为空'})

        # 2.1 判断用户是否存在
        user = BlogUser.objects.filter(username=username).exists()
        if user:
            return render(request, 'user/register.html', {'msg': '用户名已存在'})

        # 2.2 密码是否一样
        if password != password2:
            return render(request, 'user/register.html', {'msg': '密码不一样'})

        # 2.3 判断手机号格式
        if not re.match(r'^1[3-9]\d{9}$', phone):
            return render(request, 'user/register.html', {'msg': '手机号格式不匹配'})

        # 判断验证码是否过期
        if not smscode:
            return render(request, 'user/register.html', {'msg': '验证码过期'})

        # 判断验证码是否正确
        redis_cli = get_redis_connection()
        code = redis_cli.get(f'smscode_{phone}')
        # redis取出的数据格式是bytes形式
        if smscode != code.decode():
            return render(request, 'user/register.html', {'msg': '验证码不正确'})

        # 上传图片
        ext = os.path.splitext(avatar.name)[1]
        file_name = f'avatar_{phone}{ext}'
        avatar_path = os.path.join(BASE_DIR, 'static/uploads', file_name)
        with open(avatar_path, 'ab') as f:
            for chunk in avatar.chunks():
                f.write(chunk)

        # create 将数据原封不动存入数据库
        BlogUser.objects.create(
            username=username,
            password=make_password(password),
            avatar=f'/static/uploads/{file_name}',
            phone=phone
        )
        return redirect(reverse('user:login'))

def sms(request):
    phone = request.POST.get('phone')
    print(phone)
    sendSms.delay(phone)
    return JsonResponse({'status': 'ok'})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'user/login.html', {'msg': ''})
    elif request.method == 'POST':
        # 1,获取数据
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 2,判断数据

        # 2.0 判断数据都不能为空
        if not all([username, password]):
            return render(request, 'user/login.html', {'msg': '选项不能为空'})

        # 2.1 判断用户名是否存在
        try:
            user = BlogUser.objects.get(username=username)
        except BlogUser.DoesNotExist:
            return render(request, 'user/login.html', {'msg': '用户名或者密码错误'})

        # 2.2 判断密码是否正确
        if not check_password(password, user.password):
            return render(request, 'user/login.html', {'msg': '用户名或者密码错误'})

        # 处理逻辑
        # 用session保存用户的登陆状态
        request.session['id'] = user.id

        # # 生成token
        # create_token(user.id)

        return redirect(reverse('article:index'))


def logout_user(request):
    del request.session['id']
    return redirect('/user/login/')

@auth
def mine(request):
    return render(request, 'user/mine.html')

@auth
def edit(request):
    if request.method == 'GET':
        return render(request, 'user/edit.html', {'msg': ''})

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        avatar = request.FILES.get('avatar')
        phone = request.POST.get('phone')
        smscode = request.POST.get('smscode')
        bio = request.POST.get('bio')

        if not all([username, password, password2, avatar, phone, smscode, bio]):
            return render(request, 'user/edit.html', {'msg': '选项不能为空'})

        if password != password2:
            return render(request, 'user/edit.html', {'msg': '密码不一样'})

        if not re.match(r'^1[3-9]\d{9}$', phone):
            return render(request, 'user/edit.html', {'msg': '手机号格式不匹配'})

        if not smscode:
            return render(request, 'user/edit.html', {'msg': '验证码过期'})

        redis_cli = get_redis_connection()
        code = redis_cli.get(f'smscode_{phone}')
        if smscode != code.decode():
            return render(request, 'user/edit.html', {'msg': '验证码不正确'})

        ext = os.path.splitext(avatar.name)[1]
        file_name = f'avatar_{phone}{ext}'
        avatar_path = os.path.join(BASE_DIR, 'static/uploads', file_name)
        with open(avatar_path, 'ab') as f:
            for chunk in avatar.chunks():
                f.write(chunk)

        # create 将数据原封不动存入数据库
        BlogUser.objects.filter(id=request.users.id).update(
            username=username,
            password=make_password(password),
            avatar=f'/static/uploads/{file_name}',
            phone=phone,
            bio=bio
        )

        return redirect(reverse('user:edit'))

