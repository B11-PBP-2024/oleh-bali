from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from main.models import User, Buyer, Seller

# Create your models here.
class BuyerProfile(models.Model):
    user = models.OneToOneField(Buyer, on_delete=models.CASCADE)
    profile_picture = models.URLField(max_length=1000, blank=True, null=True)
    store_name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class SellerProfile(models.Model):
    user = models.OneToOneField(Seller, on_delete=models.CASCADE)
    profile_picture = models.URLField(max_length=1000, blank=True, null=True)
    store_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    price = models.IntegerField(default=10000)
    
    SUBDISTRICT_CHOICES = [
        ('Denpasar Selatan', 'Denpasar Selatan'),
        ('Denpasar Timur', 'Denpasar Timur'),
        ('Denpasar Barat', 'Denpasar Barat'),
        ('Denpasar Utara', 'Denpasar Utara'),
    ]

    VILLAGE_CHOICES = [
        # Denpasar Selatan
        ('Panjer', 'Panjer'),
        ('Pedungan', 'Pedungan'),
        ('Renon', 'Renon'),
        ('Sanur', 'Sanur'),
        ('Tukad Manggis', 'Tukad Manggis'),
        ('Tukad Punggawa', 'Tukad Punggawa'),

        # Denpasar Timur
        ('Dangin Puri', 'Dangin Puri'),
        ('Kesiman', 'Kesiman'),
        ('Penatih', 'Penatih'),
        ('Sumerta', 'Sumerta'),

        # Denpasar Barat
        ('Dauh Puri', 'Dauh Puri'),
        ('Padang Sambian', 'Padang Sambian'),
        ('Pemecutan', 'Pemecutan'),

        # Denpasar Utara
        ('Peguyangan', 'Peguyangan'),
        ('Tonja', 'Tonja'),
        ('Ubung', 'Ubung'),
    ]


    subdistrict = models.CharField(max_length=100, choices=SUBDISTRICT_CHOICES)
    village = models.CharField(max_length=100, choices=VILLAGE_CHOICES)
    address = models.CharField(max_length=255)
    maps = models.URLField(max_length=1000)

    
    def __str__(self):
        return self.user.username
