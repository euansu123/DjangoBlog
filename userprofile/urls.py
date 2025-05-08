from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    # 用户登录
    path('login/', views.user_login, name='login'),
    # 注销登录
    path('logout/', views.user_logout, name='logout'),
    # 用户注册
    path('register/', views.user_register, name='register'),
    # 用户修改
    path('edit/<int:id>/', views.user_edit, name='edit'),
    # 用户详情
    path('detail/<int:id>/', views.user_detail, name='detail'),
]