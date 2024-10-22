from django.db import models
from user_profile.models import BuyerProfile
from seller.models import ProductEntry
from django.utils import timezone

class ReviewEntry(models.Model):
    user = models.ForeignKey(BuyerProfile,on_delete=models.CASCADE)
    product = models.ForeignKey(ProductEntry,on_delete=models.CASCADE)
    time = models.DateField(default=timezone.now)
    review_text = models.TextField()

