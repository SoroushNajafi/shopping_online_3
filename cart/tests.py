from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .cart import Cart
from products.models import Product, Category


class CartDetailTest(TestCase):

    def setUp(self):
        product = Product.objects.create(
            category=Category.objects.create(en_title='title',
                                             fa_title='title', image='media/category/category_image/BEDROOM.jpg'),
            title='sample',
            description='sample_description',
            price=15000,
            image='media/products/product_images/Bar_Counter_Stools1.jpg',
            dimension='19cm*20cm*40cm',
            weight=20,
            characteristic='sample_characteristic'
        )
        self.product = product

    def test_cart_detail_page_url(self):
        self.client.post(reverse('cart:add_to_cart', args=[self.product.id]),
                         {'quantity': 1, 'inplace': False}, follow=True)

        response = self.client.get('/en/cart/')
        self.assertEqual(response.status_code, 200)

    def test_cart_detail_page_reverse(self):
        self.client.post(reverse('cart:add_to_cart', args=[self.product.id]),
                         {'quantity': 1, 'inplace': False}, follow=True)

        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)

    def test_cart_detail_page_content(self):
        self.client.post(reverse('cart:add_to_cart', args=[self.product.id]),
                         {'quantity': 1, 'inplace': False}, follow=True)

        response = self.client.get(reverse('cart:cart_detail'))
        self.assertContains(response, self.product.title)
        self.assertContains(response, self.product.price)

    def test_cart_detail_page_template_used(self):
        self.client.post(reverse('cart:add_to_cart', args=[self.product.id]),
                         {'quantity': 1, 'inplace': False}, follow=True)

        response = self.client.get(reverse('cart:cart_detail'))
        self.assertTemplateUsed(response, 'cart/cart_detail.html')


class AddToCartTest(TestCase):

    def setUp(self):
        product = Product.objects.create(
            category=Category.objects.create(en_title='title',
                                             fa_title='title', image='media/category/category_image/BEDROOM.jpg'),
            title='sample',
            description='sample_description',
            price=1500,
            image='media/products/product_images/Bar_Counter_Stools1.jpg',
            dimension='19cm*20cm*40cm',
            weight=20,
            characteristic='sample_characteristic'
        )
        self.product = product

    def test_add_to_cart_url(self):
        response = self.client.post(f'/en/cart/add/{self.product.id}/', {'quantity': 1, 'inplace': False}, follow=True)
        request = response.wsgi_request
        self.assertEqual(len(Cart(request)), 1)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Product added successfully')
        self.assertEqual(response.status_code, 200)

        response2 = self.client.get(reverse('cart:cart_detail'))
        self.assertContains(response2, self.product.title)

    def test_add_to_cart_reverse(self):
        response = self.client.post(reverse('cart:add_to_cart', args=[self.product.id]),
                                    {'quantity': 1, 'inplace': False}, follow=True)

        request = response.wsgi_request
        cart = Cart(request)
        self.assertEqual(len(cart), 1)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Product added successfully')
        self.assertEqual(response.status_code, 200)

        response2 = self.client.get(reverse('cart:cart_detail'))
        self.assertContains(response2, self.product.title)

    def test_add_to_cart_url_inplace_true(self):
        response = self.client.post(f'/en/cart/add/{self.product.id}/', {'quantity': 1, 'inplace': True}, follow=True)
        request = response.wsgi_request
        self.assertEqual(len(Cart(request)), 1)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'cart updated successfully')
        self.assertEqual(response.status_code, 200)

        response2 = self.client.get(reverse('cart:cart_detail'))
        self.assertContains(response2, self.product.title)

    def test_add_to_cart_reverse_inplace_true(self):
        response = self.client.post(reverse('cart:add_to_cart', args=[self.product.id]),
                                    {'quantity': 1, 'inplace': True}, follow=True)

        request = response.wsgi_request
        self.assertEqual(len(Cart(request)), 1)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'cart updated successfully')
        self.assertEqual(response.status_code, 200)

        response2 = self.client.get(reverse('cart:cart_detail'))
        self.assertContains(response2, self.product.title)


class RemoveFromCartTest(TestCase):

    def setUp(self):
        product = Product.objects.create(
            category=Category.objects.create(en_title='title',
                                             fa_title='title', image='media/category/category_image/BEDROOM.jpg'),
            title='sample',
            description='sample_description',
            price=1500,
            image='media/products/product_images/Bar_Counter_Stools1.jpg',
            dimension='19cm*20cm*40cm',
            weight=20,
            characteristic='sample_characteristic'
        )
        self.product = product

        self.client.post(reverse('cart:add_to_cart', args=[self.product.id]),
                         {'quantity': 1, 'inplace': False}, follow=True)

    def test_remove_from_cart_url(self):
        response = self.client.get(f'/en/cart/remove/{self.product.id}/', follow=True)
        request = response.wsgi_request
        self.assertEqual(len(Cart(request)), 0)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'product removed successfully')
        self.assertEqual(response.status_code, 200)

        response2 = self.client.get(reverse('cart:cart_detail'))
        self.assertNotContains(response, self.product.title)

    def test_remove_from_cart_reverse(self):
        response = self.client.get(reverse('cart:remove_from_cart', args=[self.product.id]), follow=True)
        request = response.wsgi_request
        self.assertEqual(len(Cart(request)), 0)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'product removed successfully')
        self.assertEqual(response.status_code, 200)

        response2 = self.client.get(reverse('cart:cart_detail'))
        self.assertNotContains(response, self.product.title)


class ClearCartTest(TestCase):
    def setUp(self):
        product = Product.objects.create(
            category=Category.objects.create(en_title='title',
                                             fa_title='title', image='media/category/category_image/BEDROOM.jpg'),
            title='sample',
            description='sample_description',
            price=1500,
            image='media/products/product_images/Bar_Counter_Stools1.jpg',
            dimension='19cm*20cm*40cm',
            weight=20,
            characteristic='sample_characteristic'
        )
        self.product = product

        self.client.post(reverse('cart:add_to_cart', args=[self.product.id]),
                         {'quantity': 1, 'inplace': False}, follow=True)

    def test_clear_cart_url(self):
        response = self.client.get('/en/cart/clear/', follow=True)
        request = response.wsgi_request
        self.assertEqual(len(Cart(request)), 0)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'cart cleared successfully')
        self.assertEqual(response.status_code, 200)

    def test_clear_cart_reverse(self):
        response = self.client.get(reverse('cart:clear_cart'), follow=True)
        request = response.wsgi_request
        self.assertEqual(len(Cart(request)), 0)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'cart cleared successfully')
        self.assertEqual(response.status_code, 200)

