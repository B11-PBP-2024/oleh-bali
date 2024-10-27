from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import WishlistItem
from user_profile.models import BuyerProfile
from seller.models import ProductEntry, ProductSeller
from main.models import Seller

User = get_user_model()

class WishlistTestCase(TestCase):
    def setUp(self):
        # Membuat user dan profile buyer
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.buyer_profile = BuyerProfile.objects.create(user=self.user)

        # Membuat seller
        self.seller = Seller.objects.create(username='selleruser', password='12345')

        # Membuat produk dan menyambungkan dengan seller
        self.product1 = ProductEntry.objects.create(
            product_name="Test Product 1",
            description="Description for Test Product 1",
            product_image="https://example.com/image1.jpg",
            product_category="Art"
        )
        self.product2 = ProductEntry.objects.create(
            product_name="Test Product 2",
            description="Description for Test Product 2",
            product_image="https://example.com/image2.jpg",
            product_category="Textile"
        )

        # Mengaitkan produk dengan seller dan menetapkan harga
        ProductSeller.objects.create(seller=self.seller, product=self.product1, price=12000)
        ProductSeller.objects.create(seller=self.seller, product=self.product2, price=20000)

        # Membuat item wishlist dan menambahkan product1
        self.wishlist_item = WishlistItem.objects.create(name="My Wishlist")
        self.wishlist_item.products.add(self.product1)
        self.wishlist_item.user.add(self.buyer_profile)


    def test_view_wishlist(self):
        response = self.client.get(reverse('wishlist:show_wishlist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product 1")
        self.assertContains(response, "Rp12000")

    def test_add_to_wishlist(self):
        # Menambahkan product2 ke wishlist
        self.wishlist_item.products.add(self.product2)

        # Mengambil kembali item wishlist yang diperbarui
        self.wishlist_item.refresh_from_db()

        # Memastikan product2 sekarang ada di wishlist
        self.assertIn(self.product2, self.wishlist_item.products.all())


    def test_delete_wishlist_item(self):
        # Test hapus produk dari wishlist
        response = self.client.get(reverse('wishlist:delete_wishlist_item', args=[self.wishlist_item.id]))
        self.assertRedirects(response, reverse('wishlist:show_wishlist'))

        # Memverifikasi item wishlist telah dihapus
        with self.assertRaises(WishlistItem.DoesNotExist):
            WishlistItem.objects.get(id=self.wishlist_item.id)

    def test_wishlist_total_price(self):
        # Menambahkan product2 ke wishlist
        self.wishlist_item.products.add(self.product2)

        # Mengambil kembali wishlist dan memverifikasi perhitungan total harga
        self.wishlist_item.refresh_from_db()
        response = self.client.get(reverse('wishlist:show_wishlist'))

        self.assertEqual(response.context['total_min'], 12000)
        self.assertEqual(response.context['total_max'], 20000)
        self.assertContains(response, "TOTAL: Rp12000 - Rp20000")

    def test_empty_wishlist(self):
        # Menghapus item wishlist untuk test tampilan wishlist kosong
        self.wishlist_item.delete()
        response = self.client.get(reverse('wishlist:show_wishlist'))
        self.assertContains(response, "No items in your wishlist.", status_code=200)