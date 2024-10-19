import uuid
from django.db import models
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
    product_name = models.CharField(max_length=255)
    price = models.IntegerField()  # Hapus auto_now_add=True
    description = models.TextField()
    product_image = models.TextField()
    product_category = models.CharField(choices=categories_choices, max_length=255)

    @property
    def is_product_strong(self):
        return self.product_intensity > 5