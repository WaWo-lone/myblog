from audioop import reverse

from django.db import models

# Create your models here.
from user.models import BlogUser

# timezone 用于处理时间相关事务。
from django.utils import timezone

from django import forms

from PIL import Image

# 引入imagekit
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


# 文章栏目
class ArticleColumn(models.Model):
    """
    栏目的 Model
    """
    # 栏目标题
    title = models.CharField(max_length=100, blank=True)
    # 创建时间
    created = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = 'articlecolumn'
        verbose_name_plural = '文章栏目'

    def __str__(self):
        return self.title


# 博客文章数据模型
class ArticlePost(models.Model):
    #     # 文章标题图
    # avatar = ProcessedImageField(
    #     verbose_name='标题图',
    #     upload_to='static/media/%Y%m%d',
    #     processors=[ResizeToFit(width=400)],
    #     format='JPEG',
    #     options={'quality': 100}
    # )

    # 文章作者。参数 on_delete 用于指定数据删除的方式
    author = models.ForeignKey(BlogUser, on_delete=models.CASCADE, verbose_name='作者', related_name='articles')

    # 文章标题。
    title = models.CharField(max_length=100, verbose_name='文章标题')

    # 文章正文。保存大量文本使用 TextField
    body = models.TextField(verbose_name='文章正文')

    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    # 浏览量
    total_views = models.PositiveIntegerField(default=0, verbose_name='浏览量')

    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )

    class Meta:
        db_table = 'article'
        ordering = ('-created',)
        # verbose_name = '文章'
        verbose_name_plural = '文章'

    def __str__(self):
        return self.title

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])

    # 保存时处理图片
    # def save(self, *args, **kwargs):
    #     # 调用原有的 save() 的功能
    #     article = super(ArticlePost, self).save(*args, **kwargs)
    #
    #     # 固定宽度缩放图片大小
    #     if self.avatar and not kwargs.get('update_fields'):
    #         image = Image.open(self.avatar)
    #         (x, y) = image.size
    #         new_x = 400
    #         new_y = int(new_x * (y / x))
    #         resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
    #         resized_image.save(self.avatar.path)
    #     return article



# 写文章的表单类
class ArticlePostForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = ArticlePost

        # 定义表单包含的字段
        fields = ('title', 'body')

