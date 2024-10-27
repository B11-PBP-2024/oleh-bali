from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from seller.models import ProductEntry, ProductSeller
from see_stores.models import Store
from user_profile.models import SellerProfile

User = get_user_model()

class SeeStoresTestCase(TestCase):
    def setUp(self):
        # Buat user, seller, dan profile seller
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        
        # Buat user dan profile seller
        self.seller_user = User.objects.create_user(username='selleruser', password='12345')
        self.seller_profile = SellerProfile.objects.create(
            user=self.seller_user,
            profile_picture="https://example.com/seller_image.jpg",
            store_name="Test Store",
            address="Jl. Contoh",
            village="Desa Contoh",
            subdistrict="Kecamatan Contoh",
            city="Kota Contoh",
            maps="https://goo.gl/maps/example"
        )

        # Buat produk
        self.product = ProductEntry.objects.create(
            product_name="Test Product",
            description="Description for Test Product",
            product_image="https://example.com/product_image.jpg",
            product_category="Art"
        )

        # Kaitkan produk dengan seller dan harga
        ProductSeller.objects.create(seller=self.seller_user, product=self.product, price=15000)

        # Buat toko yang dimiliki oleh seller_user
        self.store = Store.objects.create(
            owner=self.seller_user,
            store_name="Test Store",
            street_address="Jl. Contoh No.1",
            village="Desa Contoh",
            subdistrict="Kecamatan Contoh",
            city="Kota Contoh",
            google_maps_link="https://goo.gl/maps/example"
        )

    def test_see_stores_view(self):
        response = self.client.get(reverse('see_stores:see_stores', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")
        self.assertContains(response, "Test Store")
        self.assertContains(response, "Rp.15000")
        self.assertContains(response, "Jl. Contoh")

    def test_no_stores_available(self):
        # Hapus toko dari penjual
        ProductSeller.objects.filter(product=self.product).delete()

        response = self.client.get(reverse('see_stores:see_stores', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No stores available for this product.")

    def test_store_google_maps_link(self):
        response = self.client.get(reverse('see_stores:see_stores', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "https://goo.gl/maps/example")

