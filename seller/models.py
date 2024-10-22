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

# Model untuk Penjual (Seller)
class Seller(models.Model):
    username = models.CharField(max_length=255)

    def __str__(self):
        return self.username

# Model untuk menyimpan dataset produk yang sudah ada
class ProductDataSet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    product_image = models.TextField()
    product_category = models.CharField(choices=categories_choices, max_length=255)

    def __str__(self):
        return self.product_name

# Model untuk Produk Entry (data produk dari pengguna atau dataset)
class ProductEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_dataset = models.ForeignKey(ProductDataSet, on_delete=models.RESTRICT, null=True, blank=True)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    price = models.IntegerField()  # Tambahkan default value
    description = models.TextField(null=True, blank=True)
    product_image = models.TextField(null=True, blank=True)
    product_category = models.CharField(choices=categories_choices, max_length=255)

    # Menyimpan harga minimum dan maksimum
    min_price = models.IntegerField()
    max_price = models.IntegerField()

    def __str__(self):
        return self.product_name if self.product_name else self.product_dataset.product_name

    # Fungsi untuk menghitung dan menyimpan harga minimum dari semua penjual untuk produk ini
    def update_min_price(self):
        sellers = ProductSeller.objects.filter(product=self)
        if sellers.exists():
            self.min_price = sellers.aggregate(models.Min('price'))['price__min']
        else:
            self.min_price = None
        self.save()

    # Fungsi untuk menghitung dan menyimpan harga maksimum dari semua penjual untuk produk ini
    def update_max_price(self):
        sellers = ProductSeller.objects.filter(product=self)
        if sellers.exists():
            self.max_price = sellers.aggregate(models.Max('price'))['price__max']
        else:
            self.max_price = None
        self.save()

# Model untuk menghubungkan penjual (Seller) dengan produk (ProductEntry)
class ProductSeller(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductEntry, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Menggunakan DecimalField

    def __str__(self):
        return f"{self.seller.username} sells {self.product.product_name} at {self.price}"

    # Override save method to automatically update min_price and max_price
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Setelah ProductSeller disimpan, perbarui min_price dan max_price pada ProductEntry terkait
        self.product.update_min_price()
        self.product.update_max_price()
