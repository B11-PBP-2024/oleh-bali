from django.shortcuts import render
from django.db.models import Sum
from .models import WishlistItem

def show_wishlist(request):
    # Fetch wishlist items for the logged-in user
    wishlist_items = WishlistItem.objects.filter(user=request.user)

    # Calculate total min and max price
    total_min = wishlist_items.aggregate(Sum('min_price'))['min_price__sum'] or 0
    total_max = wishlist_items.aggregate(Sum('max_price'))['max_price__sum'] or 0

    context = {
        'wishlist_items': wishlist_items,
        'total_min': total_min,
        'total_max': total_max,
    }
    return render(request, 'wishlist/wishlist.html', context)
