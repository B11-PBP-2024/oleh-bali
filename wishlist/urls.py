from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.show_wishlist, name='show_wishlist'),
    path('wishlist/delete/<int:id>/', views.delete_wishlist_item, name='delete_wishlist_item'),
]
