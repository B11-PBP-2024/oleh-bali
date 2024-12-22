from django.urls import path
from katalog.views import get_categories, show_catalog, get_product_by_id, product_details, get_products, filter_by_category,filter_by_keyword, search_and_filter
from . import views

app_name = 'katalog'

urlpatterns = [
    path("",show_catalog,name="show_catalog"),
    path("json/<uuid:id>",get_product_by_id,name="get_product_by_id"),
    path("json/key:<str:keyword>/cat:<str:category>",search_and_filter,name="search_and_filter"),
    path("json",get_products,name="get_products"),
    path("<uuid:id>",product_details,name="product_details"),
    path("categories",get_categories,name="get_categories"),
]