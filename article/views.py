from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from article.models import ArticleEntry
from article.forms import ArticleEntryForm
from django.http import HttpResponse
from django.core import serializers

# Create your views here.
@login_required(login_url="/login/buyer")
def show_articles(request):
    articles = ArticleEntry.objects.all()
    context = {'articles':articles}
    return render(request,"article_page.html",context)

@login_required(login_url="/login/buyer")
def create_article(request):
    form = ArticleEntryForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        article = form.save(commit=False)
        article.user = request.user
        article.text = article.text.replace("/r","/n")
        article.save()
        return redirect('article:show_articles')

    context = {'form': form}
    return render(request, "create_article.html", context)

@login_required(login_url="/login/buyer")
def json_all_article(request):
    articles = ArticleEntry.objects.all()
    return HttpResponse(serializers.serialize("json", articles), content_type="application/json")

@login_required(login_url="/login/buyer")
def json_id_article(request,id):
    article = ArticleEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", article), content_type="application/json")

