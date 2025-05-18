# 引入path
from django.urls import path
from . import views


# 正在部署的应用的名称
app_name = 'article'

urlpatterns = [
    # path函数将url映射到视图
    path('list/', views.article_list, name='article_list'),
    # 文章详情
    path('detail/<uuid:id>/', views.article_detail, name='article_detail'),
    # 文章新建
    path('create/', views.article_create, name='article_create'),
    # 文章删除
    path('delete/<uuid:id>/', views.article_delete, name='article_delete'),
    # 文章更新
    path('update/<uuid:id>/', views.article_update, name='article_update'),
    # 文章专题
    path('category/', views.article_category, name='article_category'),
    # 专题详情
    path('category/<int:id>/', views.article_category_detail, name='article_category_detail'),
    # 文章标签
    path('tags/', views.article_tags, name='article_tags'),
    # 选中标签
    path('tag/<int:id>/', views.article_tag_detail, name='article_tag_detail'),
]