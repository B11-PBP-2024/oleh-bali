from django.urls import path
from . import views

app_name = 'see_stores'

urlpatterns = [
    path('<uuid:product_id>/stores/', views.see_stores, name='see_stores'),
    path('<uuid:product_id>/stores/json/', views.get_stores_json, name='get_stores_json'),
]