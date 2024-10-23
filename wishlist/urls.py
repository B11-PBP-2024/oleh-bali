from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.show_wishlist, name='show_wishlist'),
]
