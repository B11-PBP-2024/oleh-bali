from django.forms import ModelForm
from article.models import ArticleEntry

class ArticleEntryForm(ModelForm):
    class Meta:
        model = ArticleEntry
        fields = ["title","text"]