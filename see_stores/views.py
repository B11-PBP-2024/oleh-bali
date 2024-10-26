from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from seller.models import ProductEntry, ProductSeller
from user_profile.models import SellerProfile

@login_required
def see_stores(request, product_id):
    product = get_object_or_404(ProductEntry, pk=product_id)
    
    sellers = SellerProfile.objects.filter(
        user__productseller__product=product
    ).distinct()

    sellers_with_prices = []
    for seller in sellers:
        try:
            price = ProductSeller.objects.get(seller=seller.user, product=product).price
        except ProductSeller.DoesNotExist:
            price = "N/A"
        sellers_with_prices.append({
            'seller': seller,
            'price': price
        })

    context = {
        'product': product,
        'sellers_with_prices': sellers_with_prices,
    }
    return render(request, 'see_stores/see_stores.html', context)