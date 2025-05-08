
import markdown
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
# 导入数据模型ArticlePost
from .models import ArticlePost
# 导入文章表单ArticlePostForm
from .forms import ArticlePostForm
# 导入django自带的用户模型User
from django.contrib.auth.models import User
# 
from userprofile.models import UserInfo
# 导入django自带的分页模块
from django.core.paginator import Paginator


def article_list(request):

    # 取出所有博客文章
    articles = ArticlePost.objects.filter(is_deleted=False)
    # 每页显示 1 篇文章
    paginator = Paginator(articles, 10)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    # paginator.page_range 页码列表
    context = { 'articles': articles ,'page_list':paginator.page_range}
    # 需要传递给模板（templates）的对象
    # context = { 'articles': articles }
    # render函数：载入模板，并返回context对象
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)

    # 将markdown语法渲染成html样式
    # article.body = markdown.markdown(article.body,
    #     extensions=[
    #     # 包含 缩写、表格等常用扩展
    #     'markdown.extensions.extra',
    #     # 语法高亮扩展
    #     'markdown.extensions.codehilite',
    #     # 文章目录扩展
    #     'markdown.extensions.toc',
    #     ])

    md = markdown.Markdown(
        extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 目录扩展 
        'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)

    context = { 'article': article, 'toc':md.toc }
    return render(request, 'article/detail.html', context)


def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # new_article.author = User.objects.get(id=1)
            new_article.author = UserInfo.objects.get(id=1)
            # 将新文章保存到数据库中
            new_article.save()
            # 完成后返回到文章列表
            return redirect("article:article_list")
        # 如果数据不合法，返回错误信息
        else:
            # 创建表单类实例
            article_post_form = ArticlePostForm()
            # 赋值上下文
            context = { 'article_post_form': article_post_form , 'msg':'表单填写有误，请重新填写后提交。'}
            # 返回模板
            return render(request, 'article/create.html', context)
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = { 'article_post_form': article_post_form }
        # 返回模板
        return render(request, 'article/create.html', context)
    
def article_delete(request, id):
    # # 根据 id 获取需要删除的文章
    # article = ArticlePost.objects.get(id=id)
    # # 标记文章为删除状态
    # article.is_deleted = True
    # article.save()
    # # 完成删除后返回文章列表
    # return redirect("article:article_list")
    # 安全删除文章
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.is_deleted = True
        article.save()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")
    
# 文章更新
def article_update(request, id):
    # 获取所需要具体修改的文章对象
    article = ArticlePost.objects.get(id=id)
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            # 创建表单类实例
            article_post_form = ArticlePostForm()
            # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
            context = { 'article': article, 'article_post_form': article_post_form , 'msg':"填写的文章内容有误，请重新填写！"}
            # 将响应返回到模板中
            return render(request, 'article/update.html', context)
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = { 'article': article, 'article_post_form': article_post_form }
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)