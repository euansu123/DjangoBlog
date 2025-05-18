# 引入表单类
from django import forms
# 引入文章模型
from .models import ArticlePost

from ckeditor.widgets import CKEditorWidget


# 写文章的表单类
class ArticlePostForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = ArticlePost
        # 定义表单包含的字段
        fields = ('title', 'category', 'body', 'tag')

        # 自定义字段的显示名称
        labels = {
            'title': '文章标题',
            'category': '文章分组',
            'tag': '文章标签',
            'body': '文章内容',

        }
        

        # widgets = {
        #     'body': CKEditorWidget(),  # 用 CKEditor 替代原 textarea
        # }
        widgets = {
            'body': forms.Textarea(attrs={'id': 'id_content'}),
        }


