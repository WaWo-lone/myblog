# -*- author:caoyue -*-
import os

from celery import Celery

from worker import config

# 加载django的环境
# "swiper.settings",表示自己项目主目录下的setting文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")

# 实例化celery
# 'swiper'表示celery的名字
celery_app = Celery('blog')

# 加载配置文件
celery_app.config_from_object(config)

# 自动注册任务
celery_app.autodiscover_tasks()