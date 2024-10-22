from django.urls import path
from .views import show_products, add_product, upload_csv

app_name = 'seller'

urlpatterns = [
    path('', show_products, name='show_products'),        # Menampilkan daftar produk
    path('add-product/', add_product, name='add_product'),  # Tetap dengan add-product
    path('create/', add_product, name='add_product'),
    path('products/create/', add_product, name='add_product'),       # Alias untuk create
    path('upload-csv/', upload_csv, name='upload_csv'),   # Halaman untuk meng-upload CSV
]
