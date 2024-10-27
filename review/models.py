from django.db import models
from user_profile.models import Buyer
from seller.models import ProductEntry
from django.utils import timezone
import uuid

class ReviewEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    product = models.ForeignKey(ProductEntry,on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    review_text = models.TextField()

