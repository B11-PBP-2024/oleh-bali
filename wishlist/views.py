from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Min, Max
from user_profile.models import BuyerProfile
from .models import WishlistItem
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from seller.models import ProductEntry
from django.contrib.auth.decorators import login_required

def show_wishlist(request):
    buyer_profile = BuyerProfile.objects.get(user=request.user)
    wishlist_items = WishlistItem.objects.filter(user=buyer_profile)

    total_min = 0
    total_max = 0
    for item in wishlist_items:
        item_min = item.products.aggregate(min_price=Min('productseller__price'))['min_price']
        item_max = item.products.aggregate(max_price=Max('productseller__price'))['max_price']

        total_min += item_min or 0
        total_max += item_max or 0

    context = {
        'wishlist_items': wishlist_items,
        'total_min': total_min,
        'total_max': total_max,
    }
    return render(request, 'wishlist/wishlist.html', context)

def delete_wishlist_item(request, id):
    wishlist_item = get_object_or_404(WishlistItem, pk=id, user=request.user.buyerprofile)
    wishlist_item.delete()
    return redirect(reverse('wishlist:show_wishlist'))

@csrf_exempt
def add_to_wishlist(request):
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

@login_required
@csrf_exempt
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