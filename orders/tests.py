from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from products.models import Product, Category
from .models import Order, OrderItem


class OrderTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create(
            username='sample',
            email='testing@gmail.com',
            password='password123456789',
        )

        product = Product.objects.create(
            category=Category.objects.create(en_title='title',
                                             fa_title='title', image='media/category/category_image/BEDROOM.jpg'),
            title='sample',
            description='sample_description',
            price=20.99,
            image='media/products/product_images/Bar_Counter_Stools1.jpg',
            dimension='19cm*20cm*40cm',
            weight=20,
            characteristic='sample_characteristic'
        )
        self.product = product

        self.client.post('/en/accounts/login/', {'password': 'password123456789',
                                                 'login': 'testing@gmail.com'}, follow=True)

    def test_order_create_page_url(self):
        self.client.post(reverse('cart:add_to_cart', args=[self.product.id]), {'quantity': 1,
                                                                               'inplace': False}, follow=True)
        response = self.client.get('/en/order/create/')
        self.assertEqual(response.status_code, 200)

    def test_order_create_page_reverse(self):
        self.client.post(reverse('cart:add_to_cart', args=[self.product.id]), {'quantity': 1,
                                                                               'inplace': False}, follow=True)
        response = self.client.get(reverse('order_create'))
        self.assertEqual(response.status_code, 200)

    def test_order_create_page_content(self):
        self.client.post(reverse('cart:add_to_cart', args=[self.product.id]), {'quantity': 1,
                                                                               'inplace': False}, follow=True)
        response = self.client.get(reverse('order_create'))
        self.assertContains(response, self.product.title)
        self.assertContains(response, self.product.price)
        self.assertContains(response, 'place an order')

    def test_order_create_page_template_used(self):
        self.client.post(reverse('cart:add_to_cart', args=[self.product.id]), {'quantity': 1,
                                                                               'inplace': False}, follow=True)
        response = self.client.get(reverse('order_create'))
        self.assertTemplateUsed(response, 'orders/order_create.html')

    def test_order_create_post(self):
        self.client.post(reverse('cart:add_to_cart', args=[self.product.id]), {'quantity': 1,
                                                                               'inplace': False}, follow=True)
        response = self.client.post('/en/order/create/', {'first_name': 'sample_first',
                                                          'last_name': 'sample_last_name',
                                                          'phone_number': '0912234211',
                                                          'address': 'sample_address',
                                                          'order_note': 'sample_note'}, follow=True)

        self.assertEqual(Order.objects.all()[0].first_name, 'sample_first')
        self.assertEqual(Order.objects.all()[0].last_name, 'sample_last_name')
        self.assertEqual(OrderItem.objects.all()[0].product, self.product)
        self.assertEqual(Order.objects.all()[0], OrderItem.objects.all()[0].order)
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'your order has been submitted successfully')
