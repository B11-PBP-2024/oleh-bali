from django.urls import path
from katalog.views import show_catalog, get_product_by_id, product_details
app_name = 'katalog'

urlpatterns = [
    path("",show_catalog,name="show_catalog"),
    path("json/<uuid:id>",get_product_by_id,name="get_product_by_id"),
    path("<uuid:id>",product_details,name="product_details"),

]