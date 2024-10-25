from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from user_profile.models import SellerProfile

# Create your views here.

@login_required
def seller_list(request):
    sellers = SellerProfile.objects.all()

    search_query = request.GET.get('search', '')
    subdistrict_filter = request.GET.get('subdistrict', '')
    village_filter = request.GET.get('village', '')

    # Filter sellers based on search query, subdistrict, and village
    if search_query:
        sellers = sellers.filter(store_name__icontains=search_query)

    if subdistrict_filter:
        sellers = sellers.filter(subdistrict=subdistrict_filter)

    if village_filter:
        sellers = sellers.filter(village=village_filter)

    subdistrict_choices = SellerProfile.SUBDISTRICT_CHOICES
    village_choices = SellerProfile.VILLAGE_CHOICES

    context = {
        'sellers': sellers,
        'search_query': search_query,
        'selected_subdistrict': subdistrict_filter,
        'selected_village': village_filter,
        'subdistrict_choices': subdistrict_choices,
        'village_choices': village_choices,
    }
    return render(request, 'store/seller_list.html', context)