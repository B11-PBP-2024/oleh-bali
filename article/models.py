from django.db import models
from main.models import Buyer
import uuid

class ArticleEntry(models.model):
    user = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
# Create your models here.
