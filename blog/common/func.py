# -*- author:caoyue -*-
import base64
import hashlib
import json
import random

import requests
from django.http import JsonResponse
from django.shortcuts import redirect

from blog import config, settings
from django_redis import get_redis_connection

# 随机生成一个四位数验证码
from worker import celery_app


def getcode(num):
    start = 10 ** (num - 1)
    end = 10 ** num - 1
    return random.randint(start, end)

@celery_app.task
def sendSms(phone):
    # 云之讯链接
    url = config.YZX_URL

    # 四位数随机验证码
    code = getcode(4)

    # 云之讯的json数据的配置信息
    json_data = {
        "sid": config.YZX_SID,
        "token": config.YZX_TOKEN,
        "appid": config.YZX_APPID,
        "templateid": config.YZX_TEMPLATE_ID,
        "param": f"{code}, 180",
        "mobile": phone,
    }

    res = requests.post(url, json=json_data)
    '''
    res.text  程序自动转义的文本
    res.content  # 二进制数据
    res.json()  # 直接返回json数据
    '''

    redis_cli = get_redis_connection()

    redis_cli.set(f'smscode_{phone}', code, 180)



# 生成token
def create_token(uid):
    # 1.第一部分是头部信息，包含声明类型和加密算法
    # 固定的
    p1 = {
        'typ': 'JWT',
        'alg': 'HS256'
    }
    # base64.b64decode里面的是字节
    p1_base64 = base64.b64decode(json.dumps(p1).encode()).decode()

    # 2.包含用户信息
    p2 = {
        'uid': uid,
    }
    p2_base64 = base64.b64decode(json.dumps(p2).encode()).decode()

    # 3.sha256(p1_base64 + p2_base64 + secret_key)
    data = p1_base64 + p2_base64 + settings.SECRET_KEY
    sha256 = hashlib.sha256()
    sha256.update(data.encode())
    p3 = sha256.hexdigest()

    token = f"{p1_base64}.{p2_base64}.{p3}"
    return token


# sha256加密
def sha256_encode(p1, p2):
    data = p1 + p2 + settings.SECRET_KEY
    sha256 = hashlib.sha256()
    sha256.update(data.encode())
    p3 = sha256.hexdigest()
    return p3

# 验证token
def check_token(token):

    # token: abc.123.abc123
    data = token.split('.')
    sign = sha256_encode(data[0], data[1])
    # base64解码token第二部分，获取到用户id
    p2_base64_decode = base64.b64decode(data[1].encode()).decode()
    p2 = json.loads(p2_base64_decode)
    uid = p2['uid']
    if sign != data[2]:
        return False, uid
    return True, uid


# 装饰器，判断有没有登陆
def auth(func):
    def inner(request, *args, **kwargs):
        if not request.session.get('id'):
            return redirect('/user/login/')
        return func(request, *args, **kwargs)
    return inner
