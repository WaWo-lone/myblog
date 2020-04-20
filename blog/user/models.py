from django.db import models

# Create your models here.
class BlogUser(models.Model):
    username = models.CharField(max_length=20, verbose_name="用户名")
    password = models.CharField(max_length=100, verbose_name="密码")
    phone = models.CharField(max_length=11, verbose_name="手机号")
    avatar = models.CharField(max_length=100, verbose_name="头像路径")
    bio = models.CharField(max_length=500, verbose_name='个人简历')

    class Meta:
        db_table = 'blog_user'


