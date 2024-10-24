from django.urls import path
from .views import show_products, add_product, add_product_seller, show_product_seller, update_product_seller, delete_product_seller

app_name = 'seller'

urlpatterns = [
    path('', show_products, name='show_products'),          
    path('create/', add_product, name='add_product'), 
    path('seller/create', add_product_seller, name='add_product_seller'), 
    path('seller/', show_product_seller , name='show_product_seller'),  
    path('seller/edit/<uuid:id>', update_product_seller, name='edit_product_seller'),
    path('seller/delete/<uuid:id>', delete_product_seller, name='delete_product_seller'),
]
