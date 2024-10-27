from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

class Store(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_stores")
    store_name = models.CharField(max_length=255)
    profile_picture = models.URLField(null=True, blank=True)
    street_address = models.CharField(max_length=255)
    village = models.CharField(max_length=255)
    subdistrict = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    google_maps_link = models.URLField()

    def __str__(self):
        return self.store_name
