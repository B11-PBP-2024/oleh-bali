from django.shortcuts import render, redirect
from .models import ProductEntry
from .forms import ProductEntryForm

# View untuk menampilkan daftar produk
def show_products(request):
    products = ProductEntry.objects.all()  # Mengambil semua produk dari ProductEntry
    return render(request, 'products.html', {'products': products})

# View untuk menambahkan produk
def add_product(request):
    form = ProductEntryForm(request.POST)
    if request.method == 'POST'and form.is_valid() :
            
        form.save()
        return redirect('seller:show_products')  

    return render(request, 'create_product.html', {'form': form})
