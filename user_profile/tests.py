from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import BuyerProfile, SellerProfile

User = get_user_model()

class BuyerProfileViewTest(TestCase):

    def setUp(self):
        self.buyer_user = User.objects.create_user(username="buyer_test", password="test123")
        self.client.login(username="buyer_test", password="test123")

    def test_profile_buyer_view_get(self):
        url = reverse('user_profile:profile_buyer')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile/profile_buyer.html')
        self.assertTrue(BuyerProfile.objects.filter(user=self.buyer_user).exists())

    def test_profile_buyer_view_post(self):
        url = reverse('user_profile:profile_buyer')
        data = {
            'store_name': 'New Store Name',
            'nationality': 'American',
        }
        response = self.client.post(url, data)
        profile = BuyerProfile.objects.get(user=self.buyer_user)
        self.assertEqual(profile.store_name, 'New Store Name')
        self.assertEqual(profile.nationality, 'American')
        self.assertRedirects(response, url)


class SellerProfileViewTest(TestCase):

    def setUp(self):
        self.seller_user = User.objects.create_user(username="seller_test", password="test123")
        self.client.login(username="seller_test", password="test123")

    def test_profile_seller_view_get(self):
        url = reverse('user_profile:profile_seller')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile/profile_seller.html')
        self.assertTrue(SellerProfile.objects.filter(user=self.seller_user).exists())

    def test_profile_seller_view_post(self):
        url = reverse('user_profile:profile_seller')
        data = {
            'store_name': 'New Store Name',
            'city': 'New City',
            'subdistrict': 'Denpasar Selatan',
            'village': 'Panjer',
            'address': '123 New Address',
            'maps': 'https://maps.google.com',
        }
        response = self.client.post(url, data)
        profile = SellerProfile.objects.get(user=self.seller_user)
        self.assertEqual(profile.store_name, 'New Store Name')
        self.assertEqual(profile.city, 'New City')
        self.assertEqual(profile.address, '123 New Address')
        self.assertRedirects(response, url)

