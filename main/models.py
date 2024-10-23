from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

# Create your models here.
class User(AbstractUser):
    role = models.IntegerField()
    base_role = 0

    def save(self, *args, **kwargs):
        if not self.pk and self.role is None:
            self.role = self.base_role
        super().save(*args, **kwargs)

class BuyerManager(BaseUserManager):
    def get_queryset(self,*args,**kwargs):
        queryset = super().get_queryset(*args,**kwargs)
        return queryset.filter(role=0)

class Buyer(User):
    buyers = BuyerManager()
    base_role = 0
    class Meta:
        proxy = True


class SellerManager(BaseUserManager):
    def get_queryset(self,*args,**kwargs):
        queryset = super().get_queryset(*args,**kwargs)
        return queryset.filter(role=1)

class Seller(User):
    sellers = SellerManager()
    base_role = 1
    class Meta:
        proxy = True


