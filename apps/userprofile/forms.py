# 引入表单类
from django import forms
# 引入 User 模型
from django.contrib.auth.models import User

from userprofile.models import UserInfo

# 登录表单，继承了 forms.Form 类
# forms.Form则需要手动配置每个字段，它适用于不与数据库进行直接交互的功能。用户登录不需要对数据库进行任何改动，这里继承form.Form指定需要的字段即可
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


# 用户注册表单
# 对数据库进行操作的表单应该继承forms.ModelForm，可以自动生成模型中已有的字段
class UserRegisterForm(forms.ModelForm):
    # 复写 User 的密码
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        # model = User
        model = UserInfo
        fields = ('username', 'email')

    # 对两次输入的密码是否一致进行检查
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致,请重试。")
        

class UserEditForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('phone', 'avatar', 'bio', 'email')