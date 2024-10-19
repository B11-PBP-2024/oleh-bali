from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import  User, BuyerManager, Buyer, SellerManager, Seller

admin.site.register(User)
admin.site.register(Buyer)
admin.site.register(Seller)