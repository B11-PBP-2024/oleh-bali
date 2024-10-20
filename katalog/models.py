from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from seller.models import ProductEntry
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.urls import reverse

def show_catalog(request):
    return render(request,"catalog.html")
# Create your models here.
