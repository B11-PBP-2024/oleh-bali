import uuid
from django.db import models
from main.models import Seller

categories_choices = [
    ('Textile', 'Textile'),
    ('Art', 'Art'),
    ('Handicraft', 'Handicraft'),
    ('Traditional Wear', 'Traditional Wear'),
    ('Food', 'Food'),
    ('Jewelry', 'Jewelry'),
    ('Souvenir', 'Souvenir'),
    ('Accessory', 'Accessory'),
    ('Traditional Weapon', 'Traditional Weapon'),
    ('Musical Instrument', 'Musical Instrument'),
    ('Beverage', 'Beverage'),
    ('Art', 'Art'),
]

class ProductEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=255, null=True, blank=True) 
    description = models.TextField(null=True, blank=True)
    product_image = models.TextField(null=True, blank=True)
    product_category = models.CharField(choices=categories_choices, max_length=255)

    @property
    def min_price(self):
        return self.productseller_set.aggregate(models.Min("price"))['price__min']
    @property
    def max_price(self):
        return self.productseller_set.aggregate(models.Max("price"))['price__max']
    
    def __str__(self):
        return self.product_name if self.product_name else self.product.product_name

class ProductSeller(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductEntry, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  

    def __str__(self):
        return f"{self.seller.username} sells {self.product.product_name} at {self.price}"
