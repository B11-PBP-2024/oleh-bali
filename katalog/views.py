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
    return JsonResponse(products_dictionary(products), safe=False)

def product_details(request, id):
    product = ProductEntry.objects.get(pk=id)
    context = {'product':product}
    return render(request,"product_details.html",context)

# Function untuk memfilter produk berdasarkan kategori
def filter_by_category(category,data=ProductEntry.objects):
    if category == "All Categories":
        filtered_products = data.all()
    else:
        filtered_products = data.filter(product_category=category)
    return filtered_products

# Function untuk memfilter produk berdasarkan search keyword
def filter_by_keyword(keyword,data=ProductEntry.objects):
    if(keyword=="NoSearch" or keyword==None):
        filtered_products = data.all()
    else:
        filtered_products = data.filter(
            Q(product_name__icontains=keyword) | Q(description__icontains=keyword)
        )
    return filtered_products
def search_and_filter(request,keyword,category):
    products1 = filter_by_keyword(keyword)
    products2 = filter_by_category(category,products1)
    return JsonResponse(products_dictionary(products2), safe=False)

def products_dictionary(products):
    product_list = []
    for product in products:
        if product.min_price == 0 and product.max_price == 0 or product.min_price == None:
            price = "Price not available"
        elif product.min_price == product.max_price:
            price = f"Rp{product.min_price}"
        else:
            price = f"Rp{product.min_price} - Rp{product.max_price}"
        product_data = {
            'pk': product.id,
            'model': "seller.productentry",
            'fields': {
                'description': product.description,
                'product_name' : product.product_name,
                'product_image' : product.product_image,
                'product_category' : product.product_category,
                'price' : price
            }
        }
        product_list.append(product_data)
    return product_list
        


