from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import BuyerProfileForm, SellerProfileForm
from .models import BuyerProfile, SellerProfile
from .decorators import user_is_seller, user_is_buyer
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

# Create your views here.
@login_required
@user_is_buyer
def profile_buyer(request):
    profile_buyer, created = BuyerProfile.objects.get_or_create(user=request.user)

    # Mengatur nilai default, jika profile blm dibuat
    if created:
        profile_buyer.profile_picture = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"
        profile_buyer.store_name = request.user.username
        profile_buyer.nationality = "Not Set"
        profile_buyer.save()

    if request.method == 'POST':
        form = BuyerProfileForm(request.POST, instance=profile_buyer)
        if form.is_valid():
            form.save()
            return redirect('user_profile:profile_buyer')

    else:
        form = BuyerProfileForm(instance=profile_buyer)
    return render(request, 'profile/profile_buyer.html', {'form': form, 'profile': profile_buyer})

@login_required
@user_is_buyer
def profile_buyer_edit(request):
    profile_buyer = BuyerProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = BuyerProfileForm(request.POST, instance=profile_buyer)
        print("post")
        if form.is_valid():
            form.save()
            print("save")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('user_profile:profile_buyer')
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = BuyerProfileForm(instance=profile_buyer)
    return render(request, 'profile/profile_buyer_edit.html', {'form': form, 'profile': profile_buyer})

@login_required
@user_is_buyer
@require_http_methods(["GET", "POST"])
def api_profile_buyer(request):
    profile_buyer, created = BuyerProfile.objects.get_or_create(user=request.user)

    if created:
        profile_buyer.profile_picture = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"
        profile_buyer.store_name = request.user.username
        profile_buyer.nationality = "Not Set"
        profile_buyer.save()

    if request.method == 'POST':
        form = BuyerProfileForm(request.POST, instance=profile_buyer)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Profile updated successfully'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = BuyerProfileForm(instance=profile_buyer)
        return JsonResponse({
            'profile': {
                'store_name': profile_buyer.store_name,
                'nationality': profile_buyer.nationality,
                'profile_picture': profile_buyer.profile_picture,
            }
        })

@login_required
@user_is_seller
def profile_seller(request):
    profile_seller, created = SellerProfile.objects.get_or_create(user=request.user)

    # Mengatur nilai default nya, jika profile blm dibuat
    if created:
        profile_seller.profile_picture = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"
        profile_seller.store_name = request.user.username
        profile_seller.city = "Denpasar"
        profile_seller.subdistrict = "Denpasar Selatan"
        profile_seller.village = "Panjer"
        profile_seller.address = "Not Set"
        profile_seller.maps = "https://www.google.com/maps"
        profile_seller.save()

    if request.method == 'POST':
        form = SellerProfileForm(request.POST, instance=profile_seller)
        if form.is_valid():
            form.save()
            return redirect('user_profile:profile_seller')
    else:
        form = SellerProfileForm(instance=profile_seller)
    return render(request, 'profile/profile_seller.html', {'form': form, 'profile': profile_seller})

@login_required
@user_is_seller
def profile_seller_edit(request):
    profile_seller = SellerProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = SellerProfileForm(request.POST, instance=profile_seller)
        if form.is_valid():
            profile_seller = form.save()
            return redirect('user_profile:profile_seller')
    else:
        form = SellerProfileForm(instance=profile_seller)
    return render(request, 'profile/profile_seller_edit.html', {'form': form, 'profile': profile_seller})

@login_required
@user_is_seller
@require_http_methods(["GET", "POST"])
def api_profile_seller(request):
    profile_seller, created = SellerProfile.objects.get_or_create(user=request.user)

    if created:
        profile_seller.profile_picture = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"
        profile_seller.store_name = request.user.username
        profile_seller.city = "Denpasar"
        profile_seller.subdistrict = "Denpasar Selatan"
        profile_seller.village = "Panjer"
        profile_seller.address = "Not Set"
        profile_seller.maps = "https://www.google.com/maps"
        profile_seller.save()

    if request.method == 'POST':
        form = SellerProfileForm(request.POST, instance=profile_seller)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Profile updated successfully'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = SellerProfileForm(instance=profile_seller)
        return JsonResponse({
            'profile': {
                'store_name': profile_seller.store_name,
                'city': profile_seller.city,
                'subdistrict': profile_seller.subdistrict,
                'village': profile_seller.village,
                'address': profile_seller.address,
                'maps': profile_seller.maps,
                'profile_picture': profile_seller.profile_picture,
            }
        })