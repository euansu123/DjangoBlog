# 引入path
from django.urls import path
from . import views


# 正在部署的应用的名称
app_name = 'article'

urlpatterns = [
    # path函数将url映射到视图
    path('list/', views.article_list, name='article_list'),
    # 文章详情
    path('detail/<int:id>/', views.article_detail, name='article_detail'),
    # 文章新建
    path('create/', views.article_create, name='article_create'),
    # 文章删除
    path('delete/<int:id>/', views.article_delete, name='article_delete'),
    # 文章更新
    path('update/<int:id>/', views.article_update, name='article_update'),
]