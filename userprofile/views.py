from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegisterForm, UserEditForm
from django.contrib.auth.decorators import login_required
from .models import UserInfo

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .cleaned_data 清洗出合法数据
            data = user_login_form.cleaned_data
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                return redirect("article:article_list")
            else:
                user_login_form = UserLoginForm()
                context = { 'form': user_login_form , 'msg':'账号或密码输入有误。请重新输入~'}
                return render(request, 'userprofile/login.html', context)
        else:
            user_login_form = UserLoginForm()
            context = { 'form': user_login_form, 'msg':'账号或密码输入不合法~'}
            return render(request, 'userprofile/login.html', context)
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = { 'form': user_login_form }
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")
    

# 注销登录
def user_logout(request):
    logout(request)
    return redirect("userprofile:login")


# 用户注册
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存好数据跳转至登录页
            return redirect("userprofile:login")
        else:
            user_register_form = UserRegisterForm()
            context = { 'form': user_register_form , 'msg':"请按照格式填写用户注册表单~"}
            return render(request, 'userprofile/register.html', context)
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = { 'form': user_register_form }
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")
    

@login_required(login_url='/userprofile/login/')
def user_edit(request, id):
    user = UserInfo.objects.get(id=id)

    if request.method == 'POST':
        # 验证修改数据者，是否为用户本人
        if request.user != user:
            return HttpResponse("你没有权限修改此用户信息。")

        user_obj_form = UserEditForm(data=request.POST)
        if user_obj_form.is_valid():
            # 取得清洗后的合法数据
            user_obj_dic = user_obj_form.cleaned_data
            user.email = user_obj_dic['email']
            user.phone = user_obj_dic['phone']
            user.bio = user_obj_dic['bio']
            # 如果 request.FILES 存在文件，则保存
            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']
            user.save()
            # 带参数的 redirect()
            # return redirect("userprofile:edit", id=id)
            return redirect("userprofile:detail", id=id)
        else:
            user_obj_form = UserEditForm()
            context = { 'userform': user_obj_form, 'user': user, 'msg':"用户表单填写有误，请重新输出~" }
            return render(request, 'userprofile/edit.html', context)

    elif request.method == 'GET':
        user_obj_form = UserEditForm()
        context = { 'userform': user_obj_form, 'user': user }
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")
    
@login_required(login_url='/userprofile/login/')
def user_detail(request, id):
    if request.method == 'GET':
        user = UserInfo.objects.get(id=id)
        context = {"user":user}
        return render(request, 'userprofile/detail.html', context)
    else:
        return HttpResponse("请使用GET请求数据")