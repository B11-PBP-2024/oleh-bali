from django.urls import path
from .views import show_products, add_product

app_name = 'seller'

urlpatterns = [
    path('', show_products, name='show_products'),        
    path('create/', add_product, name='add_product'),       
]
