from django.forms import ModelForm
from article.models import ArticleEntry
from django.utils.html import strip_tags

class ArticleEntryForm(ModelForm):
    class Meta:
        model = ArticleEntry
        fields = ["img","title","text"]
    
    def clean_img(self):
        img = self.cleaned_data["img"]
        return strip_tags(img)
    def clean_title(self):
        title = self.cleaned_data["title"]
        return strip_tags(title)
    def clean_text(self):
        text = self.cleaned_data["text"]
        return strip_tags(text)