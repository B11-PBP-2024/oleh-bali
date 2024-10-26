from django.db import models
from django.conf import settings
from user_profile.models import BuyerProfile
from seller.models import ProductEntry, ProductSeller

class WishlistItem(models.Model):
    user = models.ManyToManyField(BuyerProfile)
    products = models.ManyToManyField(ProductEntry)
    name = models.CharField(max_length=100)

    @property
    def min_price(self):
        return self.products.aggregate(min_price=models.Min('productseller__price'))['min_price'] or 0

    @property
    def max_price(self):
        return self.products.aggregate(max_price=models.Max('productseller__price'))['max_price'] or 0

    def __str__(self):
        return self.name
