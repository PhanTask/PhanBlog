__author__ = '易'
import datetime
from haystack import indexes
from blog.models import BlogPost


class BlogPostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='author')
    pub_date = indexes.DateTimeField(model_attr='timestamp')

    def get_model(self):
        return BlogPost

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(timestamp__lte=datetime.datetime.now())