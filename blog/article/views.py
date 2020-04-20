import markdown
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from comment.forms import CommentForm
from comment.models import Comment
from user.models import BlogUser
from .models import ArticlePost, ArticlePostForm, ArticleColumn
from common.func import auth
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
def index(request):
    order = request.GET.get('order')
    search = request.GET.get('search')
    if search:
        if order == 'total_views':
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        search = ''
        if order == 'total_views':
            article_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            article_list = ArticlePost.objects.all()

    # 每页显示3篇文章
    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')  # 拿到页码参数
    if not page:
        page = 1
    page_num = int(page)
    current_page = paginator.page(page)  # 当前页的所有数据
    current_range = range(page_num, page_num + 5)
    if paginator.num_pages - page_num <= 5:
        current_range = range(paginator.num_pages - 4, paginator.num_pages + 1)
    if paginator.num_pages <= 5:
        current_range = range(1, paginator.num_pages + 1)

    context = {'search': search, 'current_page': current_page, 'current_range': current_range, 'order': order}

    return render(request, 'article/index.html', context)

@auth
def article_list(request):

    article_list = ArticlePost.objects.filter(author=request.users.id)

    # 每页显示3篇文章
    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')  # 拿到页码参数
    if not page:
        page = 1
    page_num = int(page)
    current_page = paginator.page(page)  # 当前页的所有数据
    current_range = range(page_num, page_num + 5)
    if paginator.num_pages - page_num <= 5:
        current_range = range(paginator.num_pages - 4, paginator.num_pages + 1)
    if paginator.num_pages <= 5:
        current_range = range(1, paginator.num_pages + 1)



    context = {'current_page': current_page, 'current_range': current_range}

    return render(request, 'article/list.html', context)

@auth
def article_detail(request, pk):

    article = ArticlePost.objects.get(id=pk)

    # 浏览量 +1
    article.total_views += 1

    # 取出文章评论
    comments = Comment.objects.filter(article=article)

    comment_form = CommentForm()

    # update_fields = []指定了数据库只更新total_views字段，优化执行效率
    article.save(update_fields=['total_views'])

    # 将markdown语法渲染成html样式
    article.body = markdown.markdown(article.body,
         extensions=[
         # 包含 缩写、表格等常用扩展
         'markdown.extensions.extra',
         # 语法高亮扩展
         'markdown.extensions.codehilite',
         ])

    context = {'article': article, 'pk': pk, 'comments': comments, 'comment_form': comment_form, 'msg': ''}
    # print(context)

    return render(request, 'article/detail.html', context)

@auth
def article_add(request):

    if request.method == 'GET':
        article_post_form = ArticlePostForm()
        # 文章栏目
        columns = ArticleColumn.objects.all()
        context = {'article_post_form': article_post_form, 'msg': '', 'columns': columns}
        return render(request, 'article/add.html', context)

    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST)

        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)

            # 指定登录的用户为作者
            new_article.author = BlogUser.objects.get(id=request.users.id)

            if request.POST['column'] != 'none':
                # 保存文章栏目
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])

            # 将新文章保存到数据库中
            new_article.save()

            return redirect(reverse('article:article_list'))
        else:
            return render(request, 'article/add.html', {'msg': '表单内容有误，请重新填写'})


@auth
def article_delete(request, pk):
    article = ArticlePost.objects.get(id=pk)
    if request.users != article.author:
        return HttpResponse("抱歉，你无权删除这篇文章。")
    article.delete()
    return redirect(reverse('article:article_list'))

@auth
def article_update(request, pk):
    article = ArticlePost.objects.get(id=pk)
    if request.users != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    if request.method == 'GET':
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        # print(columns)
        context = {'columns': columns, 'article': article, 'article_post_form': article_post_form}
        return render(request, 'article/update.html', context)

    if request.method == 'POST':

        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST)

        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']

            if request.POST['column'] != 'none':
                # 保存文章栏目
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None

            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect(reverse("article:article_detail", args=pk))
        # 如果数据不合法，返回错误信息
        else:
            return render(request, 'article/update.html', {'msg': '表单内容有误，请重新填写。'})

