from django.db import models
from user_profile.models import BuyerProfile
from seller.models import ProductEntry

class Like(models.Model):
    user = models.ManyToManyField(BuyerProfile)
    product = models.ManyToManyField(ProductEntry)
