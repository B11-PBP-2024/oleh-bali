from django.test import TestCase, Client
from django.urls import reverse
from main.models import Seller
from seller.models import ProductEntry, ProductSeller
from seller.forms import ProductEntryForm, ProductSellerForm
import uuid

class SellerViewsTest(TestCase):
    def setUp(self):
        self.seller = Seller.objects.create(username="TestSeller", email="seller@example.com")
        self.client = Client()
        self.client.force_login(self.seller)  

        self.product_entry = ProductEntry.objects.create(
            product_name="Test Product",
            description="Test Description",
            product_image="http://example.com/product.jpg",
            product_category="Textile"
        )

        self.product_seller = ProductSeller.objects.create(
            seller=self.seller,
            product=self.product_entry,
            price=10000
        )

    def test_show_products_view(self):
        response = self.client.get(reverse('seller:show_products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_products_entry.html')
        self.assertIn('products', response.context)

    def test_add_product_view_get(self):
        response = self.client.get(reverse('seller:add_product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_product_entry.html')
        self.assertIsInstance(response.context['form'], ProductEntryForm)

    def test_add_product_view_post(self):
        form_data = {
            'product_name': 'New Product',
            'description': 'New Description',
            'product_image': 'http://example.com/new-product.jpg',
            'product_category': 'Textile',
            'price': 20000,
        }
        response = self.client.post(reverse('seller:add_product'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('seller:show_product_seller'))

    def test_add_product_invalid_post(self):
        """Test POST request to add_product with invalid data"""
        form_data = {
            'product_name': '',  
            'description': '',
            'product_image': '',
            'product_category': '',
            'price': '',
        }
        response = self.client.post(reverse('seller:add_product'), data=form_data)
        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, 'create_product_entry.html')
        self.assertFalse(response.context['form'].is_valid())
        self.assertIn('product_name', response.context['form'].errors)

    def test_add_product_seller_view_get(self):
        response = self.client.get(reverse('seller:add_product_seller'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_product_seller.html')
        self.assertIsInstance(response.context['form'], ProductSellerForm)

    def test_add_product_seller_view_post(self):
        form_data = {
            'product': self.product_entry.id,
            'price': 15000,
        }
        response = self.client.post(reverse('seller:add_product_seller'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('seller:show_product_seller'))

    def test_add_product_seller_invalid_post(self):
        """Test POST request to add_product_seller with invalid data"""
        form_data = {
            'product': '',  
            'price': '',
        }
        response = self.client.post(reverse('seller:add_product_seller'), data=form_data)
        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, 'create_product_seller.html')
        self.assertFalse(response.context['form'].is_valid())
        self.assertIn('product', response.context['form'].errors)

    def test_show_product_seller_view(self):
        response = self.client.get(reverse('seller:show_product_seller'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_products_seller.html')
        self.assertIn('products_seller', response.context)
        self.assertIn('categories', response.context)

    def test_update_product_seller_view_post(self):
        response = self.client.post(reverse('seller:update_product_seller', args=[self.product_seller.id]), {'price': 12000})
        self.assertEqual(response.status_code, 302)
        self.product_seller.refresh_from_db()
        self.assertEqual(self.product_seller.price, 12000)

    def test_delete_product_seller_view_post(self):
        response = self.client.post(reverse('seller:delete_product_seller', args=[self.product_seller.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ProductSeller.objects.filter(id=self.product_seller.id).exists())

    def test_product_search_view(self):
        response = self.client.get(reverse('seller:product_search'), {
            'search': 'Test Product',
            'category': 'Textile',
            'sort_price': 'asc'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        products_seller = response.json()
        self.assertTrue(len(products_seller) > 0)
        self.assertEqual(products_seller[0]['product__product_name'], 'Test Product')


class ProductEntryFormTest(TestCase):
    def test_product_entry_form_valid_data(self):
        form_data = {
            'product_name': 'Test Product',
            'description': 'This is a test product',
            'product_image': 'http://example.com/product.jpg',
            'product_category': 'Textile',
            'price': 10000
        }
        form = ProductEntryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_product_entry_form_missing_fields(self):
        form_data = {
            'product_name': '',
            'description': '',
            'product_image': '',
            'product_category': '',
            'price': ''
        }
        form = ProductEntryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('product_name', form.errors)
        self.assertIn('description', form.errors)
        self.assertIn('product_image', form.errors)
        self.assertIn('product_category', form.errors)


class ProductSellerFormTest(TestCase):
    def setUp(self):
        self.seller = Seller.objects.create(username="TestSeller", email="seller@example.com")
        self.product = ProductEntry.objects.create(
            product_name="Test Product",
            description="This is a test product",
            product_image="http://example.com/product.jpg",
            product_category="Textile"
        )

    def test_product_seller_form_valid_data(self):
        form_data = {
            'product': self.product.id,
            'price': 15000,
        }
        form = ProductSellerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_product_seller_form_missing_price(self):
        form_data = {
            'product': self.product.id,
            'price': '',
        }
        form = ProductSellerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_product_seller_form_missing_product(self):
        form_data = {
            'product': '',
            'price': 15000,
        }
        form = ProductSellerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('product', form.errors)


class ProductEntryAdditionalTests(TestCase):
    def setUp(self):
        self.seller = Seller.objects.create(username="TestSeller", email="seller@example.com")
        self.product = ProductEntry.objects.create(
            product_name="Another Product",
            description="This is another test product",
            product_image="http://example.com/another-product.jpg",
            product_category="Food"
        )

    def test_empty_min_price(self):
        self.assertIsNone(self.product.min_price)

    def test_empty_max_price(self):
        self.assertIsNone(self.product.max_price)

    def test_price_display_no_sellers(self):
        self.assertIsNone(self.product.price_display)

    def test_str_method_without_name(self):
        self.product.product_name = ''
        self.product.save()
        self.assertEqual(str(self.product), 'Another Product')


class ProductSellerEdgeCasesTest(TestCase):
    def setUp(self):
        self.seller = Seller.objects.create(username="TestSellerEdge", email="selleredge@example.com")
        self.product = ProductEntry.objects.create(
            product_name="Edge Product",
            description="Edge test product",
            product_image="http://example.com/edge-product.jpg",
            product_category="Art"
        )

    def test_high_price(self):
        high_price_seller = ProductSeller.objects.create(seller=self.seller, product=self.product, price=1000000000)
        self.assertEqual(high_price_seller.price, 1000000000)
