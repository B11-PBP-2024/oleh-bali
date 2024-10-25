from django.urls import path
from .views import show_products, add_product, add_product_seller, show_product_seller

app_name = 'seller'

urlpatterns = [
    path('', show_products, name='show_products'),        
    path('create/', add_product, name='add_product'), 
    path('seller/create', add_product_seller, name='add_product_seller'), 
    path('seller/', show_product_seller , name='show_product_seller'),  
]
