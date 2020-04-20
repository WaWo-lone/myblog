from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse

from article.models import ArticlePost
from comment.forms import CommentForm
from comment.models import Comment
from common.func import auth



@auth
def post_comment(request, article_id, parent_comment_id):
    article = get_object_or_404(ArticlePost, id=article_id)

    # if request.method == 'GET':
    #     comment_form = CommentForm()
    #     context = {
    #         'comment_form': comment_form,
    #         'article_id': article_id,
    #         'parent_comment_id': parent_comment_id
    #     }
    #     print(parent_comment_id, type(parent_comment_id))
    #     return render(request, 'comment/reply.html', context)

    if request.method == 'POST':

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.users

            if parent_comment_id != '0':
                print(parent_comment_id, type(parent_comment_id))
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回复层级超过二级，则转换为二级
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                return redirect(reverse('article:article_detail', args=article_id))

                # return JsonResponse({"code": "200 OK", "new_comment_id": new_comment.id})

            new_comment.save()
            return redirect(reverse('article:article_detail', args=article_id))
        else:
            return render(request, 'article/detail.html', {'msg': "表单内容有误，请重新填写。"})
    else:
        return HttpResponse('仅接受POST请求')
