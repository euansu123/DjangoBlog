import uuid
from django.db import models
# 导入内建的User模型。
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务。
from django.utils import timezone

from django.conf import settings

from ckeditor.fields import RichTextField
# 上传功能
from ckeditor_uploader.fields import RichTextUploadingField
from pip._vendor.rich.markup import Tag


class Category(models.Model):
    """
    文章分组模型
    """
    # 分类名
    name = models.CharField(max_length=100, unique=True)
    # 分组图标
    icon = models.ImageField(upload_to='category/%Y%m%d/', blank=True)
    # 分组描述
    description = models.TextField(max_length=500, blank=True)
    # 创建时间
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ArticleTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# 博客文章数据模型
class ArticlePost(models.Model):
    # 主键设置
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 文章作者。参数 on_delete 用于指定数据删除的方式
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # 文章标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=100)

    # 文章正文。保存大量文本使用 TextField
    # body = models.TextField()
    # 设置富文本
    # body = RichTextField()
    body = RichTextUploadingField(verbose_name='文章内容', config_name='default')
    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)

    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    # 标记文章是否被删除
    is_deleted = models.BooleanField(default=False)

    # 文章分组
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # 文章标签（一个文章可以存在多个标签）
    tag = models.ManyToManyField(ArticleTag, blank=True)
    
    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        ordering = ('-created',)
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列

    def _create(self):
        """创建文章的方法，关联分类和标签"""



    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        return self.title
        # return self.title 将文章标题返回



