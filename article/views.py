from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from article.models import ArticleEntry
from article.forms import ArticleEntryForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse

# Create your views here.

def show_articles(request):
    articles = ArticleEntry.objects.all()
    context = {
        'articles':articles,
        'user':request.user}
    return render(request,"article_page.html",context)


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


def json_all_article(request):
    articles = ArticleEntry.objects.all()
    return HttpResponse(serializers.serialize("json", articles), content_type="application/json")


def json_id_article(request,id):
    article = ArticleEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", article), content_type="application/json")


def delete_article(request,id):
    article = ArticleEntry.objects.get(pk=id)
    if request.user != article.user:
        return redirect("article:show_articles")
    article.delete()
    return redirect("article:show_articles")


def edit_article(request,id):
    article = ArticleEntry.objects.get(pk=id)
    if request.user != article.user:
        return redirect("article:show_articles")
    form = ArticleEntryForm(request.POST or None,instance=article)
    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('article:show_articles'))
    return render(request,"edit_article.html",{'form':form})
