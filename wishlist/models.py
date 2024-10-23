from django.db import models
from django.conf import settings
from user_profile.models import BuyerProfile
from seller.models import ProductEntry 

class WishlistItem(models.Model):
    user = models.ManyToManyField(BuyerProfile)
    products = models.ManyToManyField(ProductEntry)
    name = models.CharField(max_length=100)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name
