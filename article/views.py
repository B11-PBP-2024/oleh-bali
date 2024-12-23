from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from article.models import ArticleEntry
from article.forms import ArticleEntryForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.urls import reverse
from user_profile.models import BuyerProfile
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

# Create your views here.

def show_articles(request):
    profile = BuyerProfile.objects.get(user=request.user)
    context = {
        'profile':profile,
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
    article_list = []
    for article in articles:
        user = BuyerProfile.objects.get(user=article.user)
        article_data = {
            'id': article.id,
            'title': article.title,
            'img':article.img,
            'text': article.text,
            'time': article.time.strftime("%B %d, %Y %H:%M"),
            'user': {
                'displayname':user.store_name,
                'profilepicture' : user.profile_picture,
                'nationality' : user.nationality
            }
        }
        article_list.append(article_data)
    return JsonResponse(article_list, safe=False)

def json_user_article(request):
    articles = ArticleEntry.objects.filter(user=request.user)
    article_list = []
    for article in articles:
        user = BuyerProfile.objects.get(user=article.user)
        article_data = {
            'id': article.id,
            'title': article.title,
            'img':article.img,
            'text': article.text,
            'time': article.time.strftime("%B %d, %Y %H:%M"),
            'user': {
                'displayname':user.store_name,
                'profilepicture' : user.profile_picture,
                'nationality' : user.nationality
            }
        }
        article_list.append(article_data)
    return JsonResponse(article_list, safe=False)

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
    return render(request,"edit_article.html",{'form':form,'article':article})

@csrf_exempt
def create_article_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        new_mood = ArticleEntry.objects.create(
            user=request.user,
            img=data["img"],
            title=data["title"],
            text=data["text"].replace("/r","/n")
        )

        new_mood.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def delete_mobile(request,id):
    if request.method == 'GET':
        article = ArticleEntry.objects.get(pk=id)
        if request.user != article.user:
            return JsonResponse({"status": "error"}, status=401)
        article.delete()
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import ArticleEntry
from .forms import ArticleEntryForm

@csrf_exempt
def edit_article_mobile(request, id):
    try:
        article = ArticleEntry.objects.get(id=id)
    except ArticleEntry.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Article not found"}, status=404)

    if request.method == "POST":
        data = json.loads(request.body)
        form = ArticleEntryForm(data, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.text = article.text.replace("/r", "/n")
            article.save()
            return JsonResponse({"status": "success"}, status=200)
        else:
            return JsonResponse({"status": "error", "message": "Invalid data"}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)