from django.contrib import admin

# Register your models here.
from .models import  ProductEntry, ProductSeller


# Register your models here.
admin.site.register(ProductEntry)
admin.site.register(ProductSeller)