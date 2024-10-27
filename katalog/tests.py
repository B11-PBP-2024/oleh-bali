from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from seller.models import ProductEntry
from user_profile.models import BuyerProfile
from wishlist.models import WishlistItem
from like.models import Like
from django.utils import timezone

User = get_user_model()

class KatalogAppTests(TestCase):

    def setUp(self):
      
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.buyer_profile = BuyerProfile.objects.create(user=self.user)
        self.client.login(username='testuser', password='password')
        
        
        self.product1 = ProductEntry.objects.create(
            product_name="Sample Product 1",
            description="This is a sample product description.",
            product_category="Category1",
            product_image="http://example.com/image1.jpg",
        )
        self.product2 = ProductEntry.objects.create(
            product_name="Sample Product 2",
            description="Another product description.",
            product_category="Category2",
            product_image="http://example.com/image2.jpg",
        )
        
        
        self.catalog_url = reverse('katalog:show_catalog')
        self.product_details_url = reverse('katalog:product_details', args=[self.product1.id])
        self.get_product_by_id_url = reverse('katalog:get_product_by_id', args=[self.product1.id])
        self.get_products_url = reverse('katalog:get_products')
        self.search_and_filter_url = reverse('katalog:search_and_filter', args=["Sample", "Category1"])

    def test_show_catalog_view(self):
        response = self.client.get(self.catalog_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog.html')
        self.assertIn('products', response.context)
        self.assertIn('categories', response.context)

    def test_product_details_view(self):
        response = self.client.get(self.product_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_details.html')
        self.assertContains(response, "Sample Product 1")
        
    def test_get_product_by_id_view(self):
        response = self.client.get(self.get_product_by_id_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertContains(response, self.product1.product_name)
        
    def test_get_products_json_view(self):
        response = self.client.get(self.get_products_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn("Sample Product 1", str(response.content))
        self.assertIn("Sample Product 2", str(response.content))

    def test_search_and_filter_view(self):
        response = self.client.get(self.search_and_filter_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn("Sample Product 1", str(response.content))
        self.assertNotIn("Sample Product 2", str(response.content))

    def test_product_like_status(self):
        Like.objects.create(user=self.buyer_profile, product=self.product1)
        response = self.client.get(self.product_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1") 
        
    def test_product_wishlist_status(self):
        wishlist_item = WishlistItem.objects.create(name="Test Wishlist")
        wishlist_item.user.add(self.buyer_profile)
        wishlist_item.products.add(self.product1)
        
        response = self.client.get(self.product_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Product 1")
        self.assertIn('is_wishlist', response.context)
        self.assertTrue(response.context['is_wishlist'])
