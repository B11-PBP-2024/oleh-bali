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
]

class ProductEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=255, null=True, blank=True) 
    description = models.TextField(null=True, blank=True)
    product_image = models.URLField(null=True, blank=True)
    product_category = models.CharField(choices=categories_choices, max_length=255)

    @property
    def min_price(self):
        return self.productseller_set.aggregate(models.Min("price"))['price__min']

    @property
    def max_price(self):
        return self.productseller_set.aggregate(models.Max("price"))['price__max']
    
    @property
    def price_display(self):
        min_price = self.min_price
        max_price = self.max_price
        
        if min_price is None and max_price is None:
            return None  
        elif min_price == max_price:
            return f"Rp{min_price:,}"
        else:
            return f"Rp{min_price:,} - Rp{max_price:,}"

    def __str__(self):
        return self.product_name if self.product_name else self.product.product_name

class ProductSeller(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductEntry, on_delete=models.CASCADE)
    price = models.IntegerField()  

    def __str__(self):
        return f"{self.seller.username} sells {self.product.product_name} at {self.price}"
