from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ProductEntry, ProductSeller
from .forms import ProductEntryForm, ProductSellerForm

def show_products(request):
    products_entry = ProductEntry.objects.all()  
    return render(request, 'show_products_entry.html', {'products': products_entry})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductEntryForm(request.POST)
        if form.is_valid():
            new_product = form.save()

            price = form.cleaned_data['price']  
            
            ProductSeller.objects.create(
                product=new_product,
                seller=request.user,
                price=price  
            )
            return redirect('seller:show_product_seller')  

    else:
        form = ProductEntryForm()  

    return render(request, 'create_product_entry.html', {'form': form})  

@login_required
def add_product_seller(request):
    form = ProductSellerForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        product_seller = form.save(commit=False)
        product_seller.seller = request.user
        product_seller.save()
        return redirect('seller:show_product_seller')

    return render(request, 'create_product_seller.html', {'form': form})

@login_required
def show_product_seller(request):

    products_seller = ProductSeller.objects.filter(seller=request.user)

    categories = dict(ProductEntry._meta.get_field('product_category').choices) 

    return render(request, 'show_products_seller.html', {
        'products_seller': products_seller,
        'categories': categories,  
    })

@login_required
def update_product_seller(request, id):
    product = get_object_or_404(ProductSeller, id=id)
    if request.method == 'POST':
        price = request.POST.get('price')
        # form = ProductSellerForm(request.POST, instance=product)
        if price:
            product.price=price
            product.save()
    return redirect('seller:show_product_seller')

@login_required
def delete_product_seller(request, id):
    product = get_object_or_404(ProductSeller, id=id)
    if request.method == 'POST':
        product.delete()
    return redirect('seller:show_product_seller')

def product_search(request):
    search_query = request.GET.get('search', '')      
    category = request.GET.get('category')        
    sort_price = request.GET.get('sort_price') 
    products_seller = ProductSeller.objects.filter(seller=request.user).select_related('product').values(
        "id", "price", "product__id", "product__product_name", "product__product_image"
    )
    if search_query:
        products_seller = products_seller.filter(Q(product__product_name__icontains=search_query))

    if category:
        products_seller = products_seller.filter(Q(product__product_category=category))

    if sort_price == 'asc':
        products_seller = products_seller.order_by('price')
    elif sort_price == 'desc':
        products_seller = products_seller.order_by('-price')
    return JsonResponse(list(products_seller), safe=False)