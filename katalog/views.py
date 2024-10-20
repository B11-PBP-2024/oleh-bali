from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from seller.models import ProductEntry
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.urls import reverse

# Create your views here.

def show_catalog(request):
    products = ProductEntry.objects.all()
    context = {
        'products':products,
        'user':request.user}
    return render(request,"catalog.html",context)
