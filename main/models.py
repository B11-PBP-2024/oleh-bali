from django.db import models
from django.contrib.auth.models import AbstractUser
from .forms import CustomUserCreationForm

class User(AbstractUser):
    add_form = CustomUserCreationForm
    is_seller = models.BooleanField(default=False)
# Create your models here.
