from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from seller.models import ProductEntry
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.urls import reverse
from django.db.models import Q 

# Create your views here.

def show_catalog(request):
    products = ProductEntry.objects.all()
    categories = []
    for choice in ProductEntry._meta.get_field('product_category').choices:
        categories.append(choice[1])
    context = {
        'products':products,
        'user':request.user,
        'categories':categories}
    return render(request,"catalog.html",context)

def get_product_by_id(request,id):
    product = ProductEntry.objects.get(pk=id)
    return HttpResponse(serializers.serialize("json", product), content_type="application/json")

def get_products(request):
    products = ProductEntry.objects.all()
    return HttpResponse(serializers.serialize("json", products), content_type="application/json")

def product_details(request, id):
    product = ProductEntry.objects.get(pk=id)
    context = {'product':product}
    return render(request,"product_details.html",context)

# Function untuk memfilter produk berdasarkan kategori
def filter_by_category(request, category):
    if category == "All Categories":
        filtered_products = ProductEntry.objects.all()
    else:
        filtered_products = ProductEntry.objects.filter(product_category=category)
    return HttpResponse(serializers.serialize("json", filtered_products), content_type="application/json")

# Function untuk memfilter produk berdasarkan search keyword
def filter_by_keyword(request,keyword):
    if(keyword=="" or keyword==None):
        filtered_products = ProductEntry.objects.all()
    else:
        filtered_products = ProductEntry.objects.filter(
            Q(product_name__icontains=keyword) | Q(description__icontains=keyword)
        )
    return HttpResponse(serializers.serialize("json", filtered_products), content_type="application/json")
