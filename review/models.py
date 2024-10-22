from django.db import models
from main.models import Buyer

class ReviewEntry(models.Model):
    user = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    product = models.
