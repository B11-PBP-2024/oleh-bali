from django.shortcuts import render, redirect, get_object_or_404 
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import ProductEntry, ProductSeller, categories_choices
from .forms import ProductEntryForm, ProductSellerForm
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
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
            messages.success(request, "Product and price added successfully.")
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
        messages.success(request, "Product seller added successfully.")
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
    product_seller = get_object_or_404(ProductSeller, id=id)
    if request.method == 'POST':
        price = request.POST.get('price')
        try:
            price = int(price)  
        except ValueError:
            messages.error(request, "Price must be a valid integer.")
            return redirect('seller:show_product_seller')  
        
        product_seller.price = price
        product_seller.save()
        messages.success(request, "Product price updated successfully.")
        return redirect('seller:show_product_seller')

    return render(request, 'edit_product_seller.html', {'product_seller': product_seller})

@login_required
def delete_product_seller(request, id):
    product = get_object_or_404(ProductSeller, id=id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully.")
    return redirect('seller:show_product_seller')

@login_required
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

@csrf_exempt
def get_categories_json(request):
    categories = [choice[0] for choice in categories_choices]
    return JsonResponse(categories, safe=False)

@login_required
def show_products_json(request):
    category = request.GET.get('category')
    search_query = request.GET.get('search', '')
    sort_price = request.GET.get('sort_price')

    products_seller = ProductSeller.objects.filter(seller=request.user)
    
    if category:
        products_seller = products_seller.filter(product__product_category=category)
    
    if search_query:
        products_seller = products_seller.filter(
            Q(product__product_name__icontains=search_query)
        )
    
    if sort_price == 'asc':
        products_seller = products_seller.order_by('price')
    elif sort_price == 'desc':
        products_seller = products_seller.order_by('-price')
    
    products_data = [{
        'id': str(product.id),
        'product_id': str(product.product.id),
        'name': product.product.product_name,
        'price': product.price,
        'image': product.product.product_image,
        'category': product.product.product_category,
    } for product in products_seller]
    
    return JsonResponse(products_data, safe=False)

@login_required
def show_all_products_json(request):
    # Mengambil semua produk dari ProductEntry
    products = ProductEntry.objects.all()
    
    # Mengubah data produk menjadi format JSON yang sesuai
    products_data = [{
        'id': str(product.id),
        'name': product.product_name,
        'category': product.product_category,
        'image': product.product_image,
        'description': product.description,
    } for product in products]
    
    return JsonResponse(products_data, safe=False)

@csrf_exempt
@login_required
def add_product_json(request):
    if request.method == 'POST':
        try:
            # Parse form data dari request.POST
            product_entry = ProductEntry.objects.create(
                product_name=request.POST.get('product_name'),
                description=request.POST.get('product_description'),
                product_category=request.POST.get('product_category'),
                product_image=request.POST.get('product_image')
            )
            
            # Membuat instance ProductSeller dengan price
            product_seller = ProductSeller.objects.create(
                product=product_entry,
                seller=request.user,
                price=request.POST.get('price')
            )
            
            response_data = {
                'status': True,
                'message': "Product berhasil ditambahkan!",
                'product': {
                    'id': product_entry.id,
                    'product_name': product_entry.product_name,
                    'description': product_entry.description,
                    'product_category': product_entry.product_category,
                    'product_image': product_entry.product_image,
                    'price': product_seller.price
                }
            }
            return JsonResponse(response_data)
            
        except Exception as e:
            return JsonResponse({
                'status': False,
                'message': f"Terjadi kesalahan: {str(e)}"
            }, status=500)
    
    return JsonResponse({
        'status': False,
        'message': "Method tidak diizinkan"
    }, status=405)

@csrf_exempt
@login_required
def add_product_seller_json(request):
    if request.method == 'POST':
        try:
            # Mengambil data dari form-data
            product_id = request.POST.get('product')
            price = request.POST.get('price')
            
            # Validasi input
            if not product_id or not price:
                return JsonResponse({
                    'status': False,
                    'message': "Product dan price harus diisi"
                }, status=400)
            
            try:
                price = int(price)
            except ValueError:
                return JsonResponse({
                    'status': False,
                    'message': "Price harus berupa angka"
                }, status=400)
            
            # Dapatkan product dari database
            try:
                product = ProductEntry.objects.get(id=product_id)
            except ProductEntry.DoesNotExist:
                return JsonResponse({
                    'status': False,
                    'message': "Product tidak ditemukan"
                }, status=404)
            
            # Buat ProductSeller baru
            product_seller = ProductSeller.objects.create(
                product=product,
                seller=request.user,
                price=price
            )
            
            return JsonResponse({
                'status': True,
                'message': "Product seller berhasil ditambahkan!",
                'data': {
                    'id': str(product_seller.id),
                    'product_name': product_seller.product.product_name,
                    'price': product_seller.price,
                    'seller': request.user.username
                }
            }, status=201)
            
        except Exception as e:
            return JsonResponse({
                'status': False,
                'message': f"Terjadi kesalahan: {str(e)}"
            }, status=500)
    
    return JsonResponse({
        'status': False,
        'message': "Method tidak diizinkan"
    }, status=405)

@csrf_exempt
@login_required
def update_product_seller_json(request, id):
    if request.method == 'POST':
        try:
            product_seller = get_object_or_404(ProductSeller, id=id)
            price = request.POST.get('price')
            
            # Validasi input
            if not price:
                return JsonResponse({
                    'status': False,
                    'message': "Harga harus diisi"
                }, status=400)
            
            try:
                price = int(price)
            except ValueError:
                return JsonResponse({
                    'status': False,
                    'message': "Harga harus berupa angka"
                }, status=400)
            
            # Update harga produk
            product_seller.price = price
            product_seller.save()
            
            return JsonResponse({
                'status': True,
                'message': "Harga produk berhasil diperbarui!",
                'data': {
                    'id': str(product_seller.id),
                    'product_name': product_seller.product.product_name,
                    'price': product_seller.price,
                    'seller': request.user.username
                }
            }, status=200)
            
        except Exception as e:
            return JsonResponse({
                'status': False,
                'message': f"Terjadi kesalahan: {str(e)}"
            }, status=500)
    
    return JsonResponse({
        'status': False,
        'message': "Method tidak diizinkan"
    }, status=405)

@csrf_exempt
@login_required
def delete_product_seller_json(request, id):
    if request.method == 'POST':
        try:
            # Dapatkan product seller berdasarkan ID
            product_seller = get_object_or_404(ProductSeller, id=id)
            
            # Pastikan yang menghapus adalah pemilik product
            if product_seller.seller != request.user:
                return JsonResponse({
                    'status': False,
                    'message': "Anda tidak memiliki izin untuk menghapus produk ini"
                }, status=403)
            
            # Hapus product seller
            product_seller.delete()
            
            return JsonResponse({
                'status': True,
                'message': "Produk berhasil dihapus!",
                'data': {
                    'id': str(id)
                }
            }, status=200)
            
        except Exception as e:
            return JsonResponse({
                'status': False,
                'message': f"Terjadi kesalahan: {str(e)}"
            }, status=500)
    
    return JsonResponse({
        'status': False,
        'message': "Method tidak diizinkan"
    }, status=405)