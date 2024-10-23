from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ProductEntry, ProductSeller
from .forms import ProductEntryForm, ProductSellerForm

def show_products(request):
    products_entry = ProductEntry.objects.all()  
    return render(request, 'show_products_entry.html', {'products': products_entry})

def add_product(request):
    form = ProductEntryForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('seller:show_products')  

    return render(request, 'create_product_entry.html', {'form': form})

@login_required
def add_product_seller(request):
    form = ProductSellerForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        product_seller = form.save(commit=False)
        product_seller.seller = request.user
        product_seller.save()
        return redirect('seller:show_products')  

    return render(request, 'create_product_seller.html', {'form': form})

@login_required
def show_product_seller(request):
    search_query = request.GET.get('search', '')  
    price_min = request.GET.get('price_min')      
    price_max = request.GET.get('price_max')     
    category = request.GET.get('category')        

    products_seller = ProductSeller.objects.filter(seller=request.user)

    if search_query:
        products_seller = products_seller.filter(product__product_name__icontains=search_query)

    if category:
        products_seller = products_seller.filter(product__product_category__iexact=category)

    if price_min:
        products_seller = products_seller.filter(price__gte=price_min)

    if price_max:
        products_seller = products_seller.filter(price__lte=price_max)

    return render(request, 'show_products_seller.html', {
        'products_seller': products_seller,
        'search_query': search_query,
        'price_min': price_min,
        'price_max': price_max,
        'category': category,
    })
