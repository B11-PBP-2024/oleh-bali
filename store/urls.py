from django.urls import path
from .views import seller_list

app_name = 'store'

urlpatterns = [
    path('', seller_list, name='seller_list'),
]
