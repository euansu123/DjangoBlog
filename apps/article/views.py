import os
import markdown
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from datetime import datetime
# 导入数据模型ArticlePost
# from .models import ArticlePost
# 导入文章表单ArticlePostForm
from article.forms import ArticlePostForm
# 导入django自带的用户模型User
from django.contrib.auth.models import User
# 
from userprofile.models import UserInfo
# 导入django自带的分页模块
from django.core.paginator import Paginator

from article.models import ArticlePost, Category, ArticleTag

from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

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
    article = ArticlePost.objects.get(uuid=id)

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
    # 标签颜色
    tag_color = ["bg-blue", "bg-green", "bg-purple", "bg-pink", "bg-teal", "bg-gold", "bg-brown"]
    # 标签为一对多关系，需要获取对应的名称
    article.tags = [{"id":tag.id, "name": tag.name, "color":tag_color[index % len(tag_color)]} for index, tag in enumerate(article.tag.all())]
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
            # 保存标签关系
            article_post_form.save_m2m()
            # 完成后返回到文章列表
            return redirect("article:article_list")
        # 如果数据不合法，返回错误信息
        else:
            # 创建表单类实例
            article_post_form = ArticlePostForm()
            # 标签
            tags = [{"id":tag.id, "name":tag.name} for tag in ArticleTag.objects.all()]
            # 分组
            categories = [{"id":category.id, "name":category.name} for category in Category.objects.all()]
            # 赋值上下文
            context = { 'article_post_form': article_post_form , 'msg':'表单填写有误，请重新填写后提交。', 'tags':tags, 'categories':categories}
            # 返回模板
            return render(request, 'article/create.html', context)
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 标签
        tags = [{"id":tag.id, "name":tag.name} for tag in ArticleTag.objects.all()]
        # 分组
        categories = [{"id":category.id, "name":category.name} for category in Category.objects.all()]
        # 赋值上下文
        context = { 'article_post_form': article_post_form , 'msg':'表单填写有误，请重新填写后提交。', 'tags':tags, 'categories':categories}
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
        article = ArticlePost.objects.get(uuid=id)
        article.is_deleted = True
        article.save()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")
    
# 文章更新
def article_update(request, id):
    # 获取所需要具体修改的文章对象
    article = ArticlePost.objects.get(uuid=id)
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
        # 创建表单类实例，使用 instance 参数初始化表单，填充已有的数据
        article_post_form = ArticlePostForm(instance=article)
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = { 'article': article, 'article_post_form': article_post_form }
        print(context)
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)


def article_category(request):
    # 查询所有的分类
    category_query = Category.objects.all()
    # 转换所有的分类
    # category_list = [model_to_dict(category) for category in category_query]
    # 可以指定要包含的字段
    # category_list = [model_to_dict(category, fields=['name', 'description']) for category in category_query]
    category_list = [{"id":category.id, "name":category.name, "icon":category.icon, "description":category.description, "count": ArticlePost.objects.filter(category=category).count()} for category in category_query]
    context = {'categories': category_list }
    return render(request, 'article/categories.html', context)


def article_category_detail(request, id):
    context = {"status": 0, "message": "success", "category": {}, "articles": []}
    try:
        category_obj = Category.objects.get(id=id)
        context["category"] = model_to_dict(category_obj)
        # 查询与专题关联的文章
        article_query = ArticlePost.objects.filter(category=category_obj).order_by('-created')
        # 对查询到的文章进行序列化处理
        # model_to_dict 默认不会序列化主键字段
        # article_list = [model_to_dict(article, fields=['uuid', 'title', 'created']) for article in article_query]
        article_list = [{"uuid": article.uuid, "title":article.title, "created":article.created.strftime('%Y-%m-%d') } for article in article_query]
        context["articles"] = article_list
    except:
        context["status"] = 1
        context["message"] = "要获取的专题不存在"
        return JsonResponse(context)

    return render(request, 'article/category.html', context)


def article_tags(request):
    # 查询所有的文章标签
    tagQuery = ArticleTag.objects.all()
    # 标签颜色
    tag_color = ["bg-blue", "bg-green", "bg-purple", "bg-pink", "bg-teal", "bg-gold", "bg-brown"]
    # 转换所有的标签，这里需要特殊处理
    tag_list = [
        {
            "id":tag.id,
            "name":tag.name, 
            "count":tag.articlepost_set.count(), 
            "color": tag_color[index % len(tag_color)]
            } for index,tag in enumerate(tagQuery)]
    # 返回上下文
    context = {'tags': tag_list }
    return render(request, 'article/tags.html', context)

def article_tag_detail(request, id):
    """选中文章标签"""
    context = {"status": 0, "message": "success"}
    # 查询所有的文章标签
    tagQuery = ArticleTag.objects.all()
    # 标签颜色
    tag_color = ["bg-blue", "bg-green", "bg-purple", "bg-pink", "bg-teal", "bg-gold", "bg-brown"]
    # 转换所有的标签，这里需要特殊处理
    tag_list = [
        {
            "id":tag.id,
            "name":tag.name, 
            "count":tag.articlepost_set.count(), 
            "color": tag_color[index % len(tag_color)]
            } for index,tag in enumerate(tagQuery)]
    # 返回上下文
    context = {'tags': tag_list }
    try:
        # 获取标签对象
        tag_obj = ArticleTag.objects.get(id=id)
        # 获取与标签关联的文章对象
        article_query = ArticlePost.objects.filter(tag=tag_obj, is_deleted=False).order_by('-created')
        # 对查询到的文章进行序列化处理
        articles_list = [{"uuid":article.uuid, "title":article.title, "created":article.created.strftime('%Y-%m-%d')} for article in article_query]
        context["articles"] = articles_list
        context["choose"] = tag_obj.name
    except:
        context["status"] = 1
        context["message"] = "要获取的标签不存在"

    return render(request, 'article/tags.html', context)

# makrdown上传图片
@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get("editormd-image-file"):
        f = request.FILES["editormd-image-file"]
        today = datetime.now().strftime('%Y%m%d')
        path = os.path.join("uploads", "article", today, f.name)
        full_path = os.path.join(settings.MEDIA_ROOT, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        response = JsonResponse({
            "success": 1,
            "message": "上传成功",
            "url": settings.MEDIA_URL + path
        })
        # 添加跨域响应头
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"
        return response

    return JsonResponse({"success": 0, "message": "上传失败"})

from django.db.models.functions import TruncYear, TruncMonth
from django.db.models import Count

def article_archives(request):
    # 查询所有的文章，按照年份进行分组，统计每个年份的文章数量
    # articles_by_year = ArticlePost.objects.filter(is_deleted=False)\
    #     .annotate(year=TruncYear('created'))\
    #         .values('year')\
    #             .annotate(count=Count('uuid'))\
    #                 .order_by('-year')    
    # 按照年份聚合文章
    articles_by_year = ArticlePost.objects.filter(is_deleted=False)\
        .annotate(year=TruncYear('created'))\
            .values('year', 'title', 'uuid', 'created')\
                .order_by('-year', '-created')
    
    archives = {}
    date_group = []
    for article in articles_by_year:
        year = article['year'].year
        if year not in archives:
            date_group.append(year)
            archives[year] = []
        archives[year].append({"uuid":article['uuid'], "title":article['title'], "created":article['created'].strftime('%Y-%m-%d')})
        # archives[year]["count"] += 1

    context = {"archives":archives, "dateGroup": date_group}

    return render(request, 'article/archives.html', context)