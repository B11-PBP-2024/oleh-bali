from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from seller.models import ProductEntry, ProductSeller
from user_profile.models import SellerProfile
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers

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

@csrf_exempt
def get_stores_json(request, product_id):
    product = get_object_or_404(ProductEntry, pk=product_id)
    
    sellers = SellerProfile.objects.filter(
        user__productseller__product=product
    ).distinct()

    
    sellers_with_prices = []
    for seller in sellers:
        seller_dict = {
            'id': seller.user.id,
            'store_name': seller.store_name,
            'profile_picture': seller.profile_picture,
            'city': seller.city,
            'subdistrict': seller.subdistrict,
            'village' : seller.village,
            'address': seller.address,
            'maps': seller.maps,
        }

        try:
            price = ProductSeller.objects.filter(seller=seller.user, product=product)
        except ProductSeller.DoesNotExist:
            price = "N/A"
        for every_price in price:
            sellers_with_prices.append({
                'seller': seller_dict,
                'price': every_price.price
            })
    data = {
        'product': {
            'id': product.id,
            'product_name': product.product_name,
            'product_category': product.product_category,
            'description': product.description,
            'product_image': product.product_image,
        },
        'sellers_with_prices': sellers_with_prices
    }
    return JsonResponse(data, safe=False)