from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Min, Max
from user_profile.models import BuyerProfile
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from seller.models import ProductEntry
from django.contrib.auth.decorators import login_required
from like.models import Like

@csrf_exempt
@login_required
def add_like(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        if not product_id:
            return JsonResponse({'success': False, 'error': 'No product ID provided'})

        buyer_profile = get_object_or_404(BuyerProfile, user=request.user)
        product = get_object_or_404(ProductEntry, pk=product_id)

        like, created = Like.objects.get_or_create(user=buyer_profile,product=product)
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def delete_like_from_catalog(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        if not product_id:
            return JsonResponse({'success': False, 'error': 'No product ID provided'})
        like = get_object_or_404(Like, product=product_id, user=request.user.buyerprofile)
        like.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

