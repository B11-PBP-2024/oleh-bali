from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.http import HttpResponseRedirect
from review.models import ReviewEntry
from seller.models import ProductEntry
from review.forms import ReviewEntryForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
import json
from django.core import serializers
from user_profile.models import BuyerProfile

def show_review(request,id):
    product = ProductEntry.objects.get(pk=id)
    reviews = ReviewEntry.objects.filter(product=product).select_related('user', 'user__buyerprofile')
    context= {
        'reviews':reviews,
        'product':product
    }
    return render(request, "review_page.html", context)

@csrf_exempt
@require_POST
def create_review(request, id):
    try:
        data = json.loads(request.body)
        review_text = data.get("review_text", "").strip()

        if not review_text:
            return JsonResponse({'success': False, 'errors': {'review_text': ['This field is required.']}}, status=400)

        product = get_object_or_404(ProductEntry, pk=id)  # Pastikan Anda memiliki model Product
        user = request.user

        new_review = ReviewEntry(
            review_text=review_text,
            product=product,
            user=user,
        )
        new_review.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'errors': str(e)}, status=500)

    # Berhasil dibuat
    return HttpResponse(b"CREATED", status=201)

def edit_review(request,id):
    review = ReviewEntry.objects.get(pk=id)

    form = ReviewEntryForm(request.POST or None, instance=review)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('review:show_review', args=[review.product.id]))
    
    context = {'form': form}
    return render(request, "edit_review.html", context)

def delete_review(request,id):
    review = ReviewEntry.objects.get(pk=id)
    product_id = review.product.id
    print(product_id)

    review.delete()

    return HttpResponseRedirect(reverse('review:show_review', args=[product_id]))

def get_reviews(request,id):
    product = ProductEntry.objects.get(pk=id)
    this_user = BuyerProfile.objects.get(user=request.user)
    reviews = ReviewEntry.objects.filter(product=product)
    review_list = []
    for review in reviews:
        user = BuyerProfile.objects.get(user=review.user)
        review_data = {
            'id': review.id,
            'time': review.time.strftime("%B %d, %Y %H:%M"),
            'review_text':review.review_text,
            'user': {
                'displayname':user.store_name,
                'profilepicture' : user.profile_picture,
                'nationality' : user.nationality
            },
            'thisUser' : this_user.store_name,
        }
        review_list.append(review_data)
    return JsonResponse(review_list, safe=False)

