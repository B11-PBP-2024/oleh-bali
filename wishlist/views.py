from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Min, Max
from user_profile.models import BuyerProfile
from .models import WishlistItem
from .models import WishlistItem
from django.urls import reverse

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