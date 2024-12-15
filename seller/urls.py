from django.urls import path
from .views import (
    add_product,
    add_product_seller,
    show_product_seller,
    update_product_seller,
    delete_product_seller,
    product_search,
    show_products,
    get_categories_json,
    show_products_json,
    show_all_products_json,
    add_product_json,
    add_product_seller_json,
    update_product_seller_json,
    delete_product_seller_json,
)

app_name = 'seller'

urlpatterns = [  
    path('', show_product_seller , name='show_product_seller'),        
    path('create/', add_product, name='add_product'), 
    path('seller/create', add_product_seller, name='add_product_seller'),  
    path('seller/edit/<uuid:id>', update_product_seller, name='edit_product_seller'),
    path('seller/delete/<uuid:id>', delete_product_seller, name='delete_product_seller'),
    path('search/', product_search, name='product_search'),

    path('get-categories/', get_categories_json, name='get_categories_json'),
    path('seller/show-products/json/', show_products_json, name='show_products_json'),
    path('seller/show-all-products/json/', show_all_products_json, name='show_all_products_json'),
    path('create/json/', add_product_json, name='add_product_json'),
    path('seller/create/json/', add_product_seller_json, name='add_product_seller_json'),
    path('seller/edit/<uuid:id>/json/', update_product_seller_json, name='update_product_seller_json'),
    path('seller/delete/<uuid:id>/json/', delete_product_seller_json, name='delete_product_seller_json'),
]