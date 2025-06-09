# 引入表单类
from django import forms
# 引入文章模型
from .models import ArticlePost

# from ckeditor.widgets import CKEditorWidget


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
        
        widgets = {
            'body': forms.Textarea(attrs={'id': 'id_content'}),
        }

        def clean_title(self):
            title = self.cleaned_data['title']
            # 创建时检查标题是否已存在
            if ArticlePost.objects.filter(title=title).exists():
                raise forms.ValidationError('文章标题已存在，请修改后重试')
            return title

class ArticleUpdateForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ('title', 'category', 'body', 'tag')
        labels = {
            'title': '文章标题',
            'category': '文章分组',
            'tag': '文章标签',
            'body': '文章内容',
        }
        widgets = {
            'body': forms.Textarea(attrs={'id': 'id_content'}),
        }

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(instance=instance, *args, **kwargs)
        self.original_instance = instance

    def clean_title(self):
        title = self.cleaned_data['title']
        # 更新时，如果标题没有改变，则允许通过
        if self.original_instance and self.original_instance.title == title:
            return title
        # 如果标题改变，检查新标题是否与其他文章重复
        print(dir(self.original_instance))
        if ArticlePost.objects.exclude(uuid=self.original_instance.uuid).filter(title=title).exists():
            raise forms.ValidationError('文章标题已存在，请修改后重试')
        return title