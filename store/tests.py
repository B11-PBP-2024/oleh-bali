from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from user_profile.models import SellerProfile
from django.http import JsonResponse

class SellerListViewTest(TestCase):

    def setUp(self):
        # Set up client and user for authentication
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # Create Seller Profiles for testing
        self.seller1 = SellerProfile.objects.create(
            user=self.user,
            store_name="Test Store 1",
            subdistrict="Subdistrict 1",
            village="Village 1"
        )
        self.seller2 = SellerProfile.objects.create(
            user=self.user,
            store_name="Test Store 2",
            subdistrict="Subdistrict 2",
            village="Village 2"
        )

    def test_seller_list_view_with_no_filters(self):
        """Test seller list view without any filters or search"""
        response = self.client.get(reverse('seller_list'))  # Adjust reverse URL name as per your project
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/seller_list.html')
        self.assertIn('Test Store 1', response.content.decode())
        self.assertIn('Test Store 2', response.content.decode())

    def test_seller_list_view_with_search(self):
        """Test seller list view with search query"""
        response = self.client.get(reverse('seller_list'), {'search': 'Test Store 1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Store 1', response.content.decode())
        self.assertNotIn('Test Store 2', response.content.decode())

    def test_seller_list_view_with_subdistrict_filter(self):
        """Test seller list view with subdistrict filter"""
        response = self.client.get(reverse('seller_list'), {'subdistrict': 'Subdistrict 1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Store 1', response.content.decode())
        self.assertNotIn('Test Store 2', response.content.decode())

    def test_seller_list_view_with_village_filter(self):
        """Test seller list view with village filter"""
        response = self.client.get(reverse('seller_list'), {'village': 'Village 2'})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Test Store 1', response.content.decode())
        self.assertIn('Test Store 2', response.content.decode())

    def test_seller_list_view_with_combined_filters(self):
        """Test seller list view with combined subdistrict and village filters"""
        response = self.client.get(reverse('seller_list'), {'subdistrict': 'Subdistrict 2', 'village': 'Village 2'})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Test Store 1', response.content.decode())
        self.assertIn('Test Store 2', response.content.decode())

    def test_seller_list_view_ajax_request(self):
        """Test seller list view for AJAX request handling"""
        response = self.client.get(reverse('seller_list'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response, JsonResponse))
        self.assertIn('html', response.json())
        self.assertIn('Test Store 1', response.json()['html'])
        self.assertIn('Test Store 2', response.json()['html'])

    def test_seller_list_view_template(self):
        """Test the correct template is used in the view"""
        response = self.client.get(reverse('seller_list'))
        self.assertTemplateUsed(response, 'store/seller_list.html')
