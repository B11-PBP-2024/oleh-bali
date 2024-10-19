from django.db import models
from main.models import Buyer
import uuid
from django.utils import timezone

class ArticleEntry(models.Model):
    user = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    img = models.TextField()
    time = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=255)
    text = models.TextField()
# Create your models here.
