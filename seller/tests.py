from django.test import TestCase
from django.urls import reverse
from .models import ProductEntry, ProductSeller
from main.models import Seller
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductViewsTest(TestCase):

    def setUp(self):
        self.seller = Seller.objects.create(username='test_seller', email='test_seller@example.com')
        self.product_entry = ProductEntry.objects.create(
            product_name="Sample Product",
            description="This is a test product",
            product_image="http://example.com/image.jpg",
            product_category="Textile"
        )
        self.product_seller = ProductSeller.objects.create(
            seller=self.seller,
            product=self.product_entry,
            price=10000
        )

    def test_show_product_seller_view(self):
        self.client.force_login(self.seller)
        response = self.client.get(reverse('seller:show_product_seller'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Product")

    def test_add_product_view(self):
        self.client.force_login(self.seller)
        response = self.client.post(reverse('seller:add_product'), {
            'product_name': 'New Product',
            'description': 'Test description',
            'product_image': 'http://example.com/image.jpg',
            'product_category': 'Textile',
            'price': 20000
        })
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(ProductEntry.objects.count(), 2)

    def test_update_product_seller_view(self):
        self.client.force_login(self.seller)
        response = self.client.post(reverse('seller:edit_product_seller', args=[self.product_seller.id]), {
            'price': 15000
        })
        self.assertEqual(response.status_code, 302)  
        self.product_seller.refresh_from_db()
        self.assertEqual(self.product_seller.price, 15000)

    def test_delete_product_seller_view(self):
        self.client.force_login(self.seller)
        response = self.client.post(reverse('seller:delete_product_seller', args=[self.product_seller.id]))
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(ProductSeller.objects.count(), 0)
