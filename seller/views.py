from django.shortcuts import render, redirect
from .models import ProductEntry
from .forms import ProductEntryForm

def show_products(request):
    products = ProductEntry.objects.all()  
    return render(request, 'products.html', {'products': products})

def add_product(request):
    form = ProductEntryForm(request.POST)
    if request.method == 'POST'and form.is_valid() :
            
        form.save()
        return redirect('seller:show_products')  

    return render(request, 'create_product.html', {'form': form})
