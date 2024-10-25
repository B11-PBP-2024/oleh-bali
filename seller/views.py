from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
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
            # Simpan produk baru dan ambil instance-nya
            new_product = form.save()

            # Ambil harga dari form
            price = form.cleaned_data['price']  # Ambil harga yang diinputkan pengguna

            # Menyimpan ke ProductSeller
            ProductSeller.objects.create(
                product=new_product,
                seller=request.user,
                price=price  # Simpan harga yang diinputkan
            )
            return redirect('seller:show_product_seller')  # Redirect ke halaman daftar produk

    else:
        form = ProductEntryForm()  # Jika GET, buat form baru

    return render(request, 'create_product_entry.html', {'form': form})  # Kembali ke form jika GET

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
    search_query = request.GET.get('search', '')      
    category = request.GET.get('category')        
    sort_price = request.GET.get('sort_price')  

    products_seller = ProductSeller.objects.filter(seller=request.user)

    if search_query:
        products_seller = products_seller.filter(Q(product__product_name__icontains=search_query))

    if category:
        products_seller = products_seller.filter(Q(product__product_category=category))

    if sort_price == 'asc':
        products_seller = products_seller.order_by('price')
    elif sort_price == 'desc':
        products_seller = products_seller.order_by('-price')

    categories = dict(ProductEntry._meta.get_field('product_category').choices)  

    return render(request, 'show_products_seller.html', {
        'products_seller': products_seller,
        'categories': categories,  
        'search_query': search_query,
        'category': category,
        'sort_price': sort_price,
    })

@login_required
def update_product_seller(request, id):
    product = get_object_or_404(ProductSeller, id=id)
    if request.method == 'POST':
        form = ProductSellerForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('seller:show_product_seller')
    else:
        form = ProductSellerForm(instance=product)
    return render(request, 'edit_product_seller.html', {'form': form})

@login_required
def delete_product_seller(request, id):
    product = get_object_or_404(ProductSeller, id=id)
    if request.method == 'POST':
        product.delete()
    return redirect('seller:show_product_seller')
