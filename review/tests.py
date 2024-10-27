from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from review.models import ReviewEntry
from seller.models import ProductEntry
from user_profile.models import BuyerProfile
from django.utils import timezone
import json
import uuid

User = get_user_model()

class ReviewAppTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        
        # Set up test user and product
        self.user = User.objects.create_user(username="testuser", password="password")
        self.buyer_profile = BuyerProfile.objects.create(user=self.user, store_name="Test Store")
        self.client.login(username="testuser", password="password")
        
        self.product = ProductEntry.objects.create(
            product_name="Test Product",
            description="A test product.",
            product_category="Category A",
        )
        
        # Set up URLs
        self.show_review_url = reverse("review:show_review", args=[self.product.id])
        self.create_review_url = reverse("review:create_review", args=[self.product.id])
        self.edit_review_url = reverse("review:edit_review", args=[self.product.id])
        self.delete_review_url = reverse("review:delete_review", args=[self.product.id])
        self.get_reviews_url = reverse("review:get_reviews")

        # Create a sample review
        self.review = ReviewEntry.objects.create(
            user=self.user,
            product=self.product,
            review_text="This is a test review.",
            time=timezone.now()
        )

    def test_show_review_view(self):
        response = self.client.get(self.show_review_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "review_page.html")
    
    def test_create_review_view(self):
        review_data = {
            "review_text": "A new test review"
        }
        response = self.client.post(
            self.create_review_url,
            data=json.dumps(review_data),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": True})
        self.assertTrue(ReviewEntry.objects.filter(review_text="A new test review").exists())

    def test_create_review_view_missing_text(self):
        review_data = {
            "review_text": ""
        }
        response = self.client.post(
            self.create_review_url,
            data=json.dumps(review_data),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("review_text", json.loads(response.content)["errors"])

    def test_get_reviews_view(self):
        response = self.client.get(self.get_reviews_url)
        self.assertEqual(response.status_code, 200)
        reviews = json.loads(response.content)
        self.assertEqual(len(reviews), 1)
        self.assertEqual(reviews[0]["review_text"], "This is a test review.")
        self.assertEqual(reviews[0]["user"]["displayname"], self.buyer_profile.store_name)
