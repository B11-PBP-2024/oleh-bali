from django.shortcuts import render, get_object_or_404
from seller.models import ProductSeller, ProductEntry

def see_stores(request, product_id):
    product = get_object_or_404(ProductEntry, id=product_id)
    stores = ProductSeller.objects.filter(product=product).select_related('seller')
    
    context = {
        'product': product,
        'stores': stores,
    }
    return render(request, 'see_stores/see_stores.html', context)
