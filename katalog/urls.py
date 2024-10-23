from django.urls import path
from katalog.views import show_catalog, get_product_by_id, product_details, get_products, filter_by_category,filter_by_keyword
app_name = 'katalog'

urlpatterns = [
    path("",show_catalog,name="show_catalog"),
    path("json/<uuid:id>",get_product_by_id,name="get_product_by_id"),
    path("json/filter/<str:category>",filter_by_category,name="filter_by_category"),
    path("json/search/<str:keyword>",filter_by_keyword,name="filter_by_keyword"),
    path("json/search/",get_products,name="get_products"),
    path("json",get_products,name="get_products"),
    path("<uuid:id>",product_details,name="product_details"),

]