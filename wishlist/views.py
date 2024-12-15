import json
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Min, Max
from user_profile.models import BuyerProfile
from .models import WishlistItem
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from seller.models import ProductEntry
from django.contrib.auth.decorators import login_required

@login_required
def show_wishlist(request):
    buyer_profile = BuyerProfile.objects.get(user=request.user)
    wishlist_items = WishlistItem.objects.filter(user=buyer_profile)

    total_min = sum([item.min_price for item in wishlist_items])
    total_max = sum([item.max_price for item in wishlist_items])

    context = {
        'wishlist_items': wishlist_items,
        'total_min': total_min,
        'total_max': total_max,
    }
    return render(request, 'wishlist/wishlist.html', context)

@login_required
def delete_wishlist_item(request, id):
    buyer_profile = get_object_or_404(BuyerProfile, user=request.user)
    wishlist_item = get_object_or_404(WishlistItem, pk=id, user=buyer_profile)
    wishlist_item.delete()
    return redirect(reverse('wishlist:show_wishlist'))

@csrf_exempt
@login_required
def add_to_wishlist(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        if not product_id:
            product_id = json.loads(request.body).get('product_id')
        if not product_id:
            return JsonResponse({'success': False, 'error': 'No product ID provided'})

        buyer_profile = get_object_or_404(BuyerProfile, user=request.user)
        product = get_object_or_404(ProductEntry, pk=product_id)

        wishlist_item, created = WishlistItem.objects.get_or_create(name=product.product_name)

        wishlist_item.products.add(product)
        wishlist_item.user.add(buyer_profile)

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
@login_required
def add_to_wishlist_from_details(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        if not product_id:
            return JsonResponse({'success': False, 'error': 'No product ID provided'})

        buyer_profile = get_object_or_404(BuyerProfile, user=request.user)
        product = get_object_or_404(ProductEntry, pk=product_id)

        wishlist_item, created = WishlistItem.objects.get_or_create(name=product.product_name)

        wishlist_item.products.add(product)
        wishlist_item.user.add(buyer_profile)

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def delete_wishlist_item_from_catalog(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        if not product_id:
            product_id = json.loads(request.body).get('product_id')
        if not product_id:
            return JsonResponse({'success': False, 'error': 'No product ID provided'})
        wishlist_item = get_object_or_404(WishlistItem, products=product_id, user=request.user.buyerprofile)
        wishlist_item.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def get_wishlist_json(request):
    if request.method == "GET":
        buyer_profile = get_object_or_404(BuyerProfile, user=request.user)
        wishlist_items = WishlistItem.objects.filter(user=buyer_profile)
        wishlist_json = []
        for item in wishlist_items:
            wishlist_json.append({
                'name': item.name,
                'min_price': item.min_price,
                'max_price': item.max_price,
                'products': products_dictionary(item.products.all())
                
            })
        
        json_data = {
            'total_min' : sum([item.min_price for item in wishlist_items]),
            'total_max' : sum([item.max_price for item in wishlist_items]),
            'wishlists' : wishlist_json,
        }
        return JsonResponse(json_data, safe=False)
    return JsonResponse({'error': 'Invalid request method'})

def products_dictionary(products):
    product_list = []
    for product in products:
        if product.min_price == 0 and product.max_price == 0 or product.min_price == None:
            price = "Price not available"
        elif product.min_price == product.max_price:
            price = f"Rp{product.min_price}"
        else:
            price = f"Rp{product.min_price} - Rp{product.max_price}"

        
        product_data = {
            'pk': product.id,
            'model': "seller.productentry",
            'fields': {
                'description': product.description,
                'product_name' : product.product_name,
                'product_image' : product.product_image,
                'product_category' : product.product_category,
                'price' : price,
            }
        }
        product_list.append(product_data)
    return product_list