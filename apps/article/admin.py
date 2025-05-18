from django.contrib import admin
from article.models import ArticlePost, Category, ArticleTag

# 注册ArticlePost到admin中
admin.site.register(ArticlePost)
# 注册文章分类到admin中
admin.site.register(Category)
# 注册文章标签到admin中
admin.site.register(ArticleTag)