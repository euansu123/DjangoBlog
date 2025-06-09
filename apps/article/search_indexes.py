from haystack import indexes
from article.models import ArticlePost

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='author')
    title = indexes.CharField(model_attr='title')
    body = indexes.CharField(model_attr='body')
    uuid = indexes.CharField(model_attr='uuid')  # 添加这一行
    created = indexes.DateTimeField(model_attr='created')
    

    def get_model(self):
        return ArticlePost

    def index_queryset(self, using=None):
        return self.get_model().objects.all()