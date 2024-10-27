from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from user_profile.models import BuyerProfile, SellerProfile

User = get_user_model()

class MainAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create buyer and seller users
        self.buyer_user = User.objects.create_user(username='test_buyer', password='password123', role=0)
        self.seller_user = User.objects.create_user(username='test_seller', password='password123', role=1)

        # Create profiles for buyer and seller
        BuyerProfile.objects.create(user=self.buyer_user, store_name="Test Store")
        SellerProfile.objects.create(user=self.seller_user, store_name="Seller Store")
        
        self.buyer_login_url = reverse('main:login_buyer')
        self.seller_login_url = reverse('main:login_seller')
        self.main_url = reverse('main:show_main')
        self.buyer_register_url = reverse('main:register_buyer')
        self.seller_register_url = reverse('main:register_seller')
    
    def test_buyer_login(self):
        response = self.client.post(self.buyer_login_url, {'username': 'test_buyer', 'password': 'password123'})
        self.assertRedirects(response, self.main_url)
        
    def test_seller_login(self):
        response = self.client.post(self.seller_login_url, {'username': 'test_seller', 'password': 'password123'})
        self.assertRedirects(response, self.main_url)
        
    def test_show_main_view_buyer(self):
        self.client.login(username='test_buyer', password='password123')
        response = self.client.get(self.main_url)
        self.assertTemplateUsed(response, 'homepage_buyer.html')
    
    def test_show_main_view_seller(self):
        self.client.login(username='test_seller', password='password123')
        response = self.client.get(self.main_url)
        self.assertTemplateUsed(response, 'homepage_seller.html')

    def test_buyer_register_view(self):
        response = self.client.post(self.buyer_register_url, {
            'username': 'new_buyer', 'password1': 'newpassword123', 'password2': 'newpassword123'
        })
        self.assertRedirects(response, self.buyer_login_url)
        self.assertTrue(User.objects.filter(username='new_buyer').exists())

    def test_seller_register_view(self):
        response = self.client.post(self.seller_register_url, {
            'username': 'new_seller', 'password1': 'newpassword123', 'password2': 'newpassword123'
        })
        self.assertRedirects(response, self.seller_login_url)
        self.assertTrue(User.objects.filter(username='new_seller').exists())

    def test_logout_user_buyer_redirect(self):
        self.client.login(username='test_buyer', password='password123')
        response = self.client.get(reverse('main:logout_user'))
        self.assertRedirects(response, self.buyer_login_url)

    def test_logout_user_seller_redirect(self):
        self.client.login(username='test_seller', password='password123')
        response = self.client.get(reverse('main:logout_user'))
        self.assertRedirects(response, self.seller_login_url)

    def test_404_handler(self):
        response = self.client.get('/nonexistent-url/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')
