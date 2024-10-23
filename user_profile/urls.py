from django.urls import path
from .views import profile_buyer, profile_seller, profile_buyer_edit, profile_seller_edit


app_name = 'user_profile'

urlpatterns = [
    path('buyer/', profile_buyer, name='profile_buyer'),
    path('seller/', profile_seller, name='profile_seller'),
    path('buyer/edit', profile_buyer_edit, name='profile_buyer_edit'),
    path('seller/edit', profile_seller_edit, name='profile_seller_edit'),
]