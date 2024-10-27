from django.urls import path
from .views import add_like, delete_like_from_catalog

app_name = 'like'

urlpatterns = [
    path('add/', add_like, name="add_like"),
    path('delete/', delete_like_from_catalog, name="delete_like_from_catalog")
]