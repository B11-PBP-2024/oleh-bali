from django.urls import path
from .views import seller_list, api_seller_list

app_name = 'store'

urlpatterns = [
    path('', seller_list, name='seller_list'),

    path('api/seller/', api_seller_list, name='api_seller_list'),
]
