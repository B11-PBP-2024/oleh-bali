from django.shortcuts import render, redirect
from seller.forms import ProductEntryForm
from seller.models import ProductEntry

def show_products(request):

    return render(request, "products.html")# Create your views here.

def add_product(request):
    form = ProductEntryForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        product = form.save()
        return redirect("seller:show_products")
    return render(request,"create_product.html",{'form':form})
