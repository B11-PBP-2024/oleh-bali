from django.test import TestCase

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from main.models import Buyer, User
from user_profile.models import BuyerProfile
from article.models import ArticleEntry
from article.forms import ArticleEntryForm
import uuid

class ArticleAppTests(TestCase):
    
    def setUp(self):
        
        self.client = Client()
        
    
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.buyer = Buyer.objects.get(pk=self.user.pk)
        
       
        self.profile = BuyerProfile.objects.create(
            user=self.buyer,
            store_name="Test Store",
            profile_picture="http://example.com/profile.jpg",
            nationality="Testland"
        )
        
       
        self.client.login(username='testuser', password='testpassword')
        
  
        self.article = ArticleEntry.objects.create(
            user=self.buyer,
            title="Test Article",
            img="http://example.com/image.jpg",
            text="Sample content for testing.",
            time=timezone.now()
        )

    def test_create_article_view(self):
        """Test creating an article via POST request."""
        data = {
            'title': 'New Article',
            'img': 'http://example.com/new_image.jpg',
            'text': 'New content for article.'
        }
        response = self.client.post(reverse('article:create_article'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ArticleEntry.objects.filter(title='New Article').exists())

    def test_json_all_article_view(self):
        """Test JSON output for all articles."""
        response = self.client.get(reverse('article:json_all_article'))
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(isinstance(json_data, list))
        self.assertEqual(json_data[0]['title'], 'Test Article')

    def test_json_user_article_view(self):
        """Test JSON output for the user's articles only."""
        response = self.client.get(reverse('article:json_user_article'))
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(isinstance(json_data, list))
        self.assertEqual(json_data[0]['user']['displayname'], 'Test Store')

    def test_edit_article_view(self):
        """Test editing an article."""
        url = reverse('article:edit_article', kwargs={'id': self.article.id})
        response = self.client.post(url, {
            'title': 'Updated Title',
            'img': 'http://example.com/updated_image.jpg',
            'text': 'Updated text content.'
        })
        self.assertEqual(response.status_code, 302)
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Updated Title')
        self.assertEqual(self.article.img, 'http://example.com/updated_image.jpg')

    def test_delete_article_view(self):
        """Test deleting an article."""
        article_id = self.article.id
        url = reverse('article:delete_article', kwargs={'id': article_id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ArticleEntry.objects.filter(pk=article_id).exists())

    def test_access_json_id_article(self):
        """Test retrieving a single article by ID in JSON format."""
        response = self.client.get(reverse('article:json_id_article', kwargs={'id': self.article.id}))
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data[0]['fields']['title'], 'Test Article')

