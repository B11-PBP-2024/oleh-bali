from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from user_profile.models import SellerProfile
from django.http import JsonResponse

User = get_user_model()

class SellerListViewTest(TestCase):

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
        
        # Set up Seller Profiles with different attributes for testing
        SellerProfile.objects.create(
            user=self.user,
            store_name="Test Store 1",
            subdistrict="Denpasar Selatan",
            village="Panjer"
        )
        SellerProfile.objects.create(
            user=self.user,
            store_name="Test Store 2",
            subdistrict="Denpasar Barat",
            village="Sumerta"
        )
        SellerProfile.objects.create(
            user=self.user,
            store_name="Another Store",
            subdistrict="Denpasar Selatan",
            village="Sumerta"
        )

    def test_seller_list_view_basic_get(self):
        url = reverse('store:seller_list')
        response = self.client.get(url)
        
        # Check that the response is successful and uses the correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/seller_list.html')
        self.assertEqual(len(response.context['sellers']), 3)

    def test_seller_list_view_search_filter(self):
        url = reverse('store:seller_list')
        response = self.client.get(url, {'search': 'Test Store'})
        
        # Expect only stores with "Test Store" in their name
        self.assertEqual(len(response.context['sellers']), 2)
        for seller in response.context['sellers']:
            self.assertIn("Test Store", seller.store_name)

    def test_seller_list_view_subdistrict_filter(self):
        url = reverse('store:seller_list')
        response = self.client.get(url, {'subdistrict': 'Denpasar Selatan'})
        
        # Expect only sellers in the specified subdistrict
        self.assertEqual(len(response.context['sellers']), 2)
        for seller in response.context['sellers']:
            self.assertEqual(seller.subdistrict, 'Denpasar Selatan')

    def test_seller_list_view_village_filter(self):
        url = reverse('store:seller_list')
        response = self.client.get(url, {'village': 'Sumerta'})
        
        # Expect only sellers in the specified village
        self.assertEqual(len(response.context['sellers']), 2)
        for seller in response.context['sellers']:
            self.assertEqual(seller.village, 'Sumerta')

    def test_seller_list_view_combined_filters(self):
        url = reverse('store:seller_list')
        response = self.client.get(url, {'search': 'Test', 'subdistrict': 'Denpasar Selatan', 'village': 'Panjer'})
        
        # Expect only sellers matching all filters
        self.assertEqual(len(response.context['sellers']), 1)
        self.assertEqual(response.context['sellers'][0].store_name, "Test Store 1")

    def test_seller_list_view_ajax_request(self):
        url = reverse('store:seller_list')
        response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        # Check that response is JSON
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        self.assertIn('html', response.json())

