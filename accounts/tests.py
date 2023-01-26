from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class SignUpViewTest(TestCase):

    def test_signup_page_url(self):
        response = self.client.get('/en/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_signup_page_reverse(self):
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_page_content(self):
        response = self.client.get('/en/accounts/signup/')
        self.assertContains(response, 'Sign up')

    def test_signup_page_template_used(self):
        response = self.client.get(reverse('account_signup'))
        self.assertTemplateUsed(response, 'account/signup.html')

    def test_signup_post(self):
        response = self.client.post('/en/accounts/signup/', {'email': 'sample_test@gmail.com',
                                                             'password1': 'pass1234sample',
                                                             'password2': 'pass1234sample', }, follow=True)

        self.assertEqual(get_user_model().objects.all()[0].email, 'sample_test@gmail.com')
        self.assertEqual(get_user_model().objects.all()[0].username, 'sample_test')
        self.assertEqual(get_user_model().objects.all().count(), 1)
        messages = list(response.context['messages'])
        print(response.context['messages'])
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]), 'Successfully signed in as sample_test.')
        self.assertEqual(response.status_code, 200)


class LoginViewTest(TestCase):
    def setUp(self):
        self.client.post('/en/accounts/signup/', {'email': 'sample_test@gmail.com',
                                                  'password1': 'pass1234sample',
                                                  'password2': 'pass1234sample', }, follow=True)

        self.client.post(reverse('account_logout'), follow=True)

    def test_login_page_url(self):
        response = self.client.get('/en/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_page_reverse(self):
        response = self.client.get(reverse('account_login'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_content(self):
        response = self.client.get(reverse('account_login'))
        self.assertContains(response, 'Login')

    def test_login_page_template_used(self):
        response = self.client.get(reverse('account_login'))
        self.assertTemplateUsed(response, 'account/login.html')

    def test_login_post(self):
        response = self.client.post('/en/accounts/login/', {'password': 'pass1234sample',
                                                            'login': 'sample_test@gmail.com'}, follow=True)

        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Successfully signed in as sample_test.')


class LogoutTest(TestCase):
    def setUp(self):
        self.client.post('/en/accounts/signup/', {'email': 'sample_test@gmail.com',
                                                  'password1': 'pass1234sample',
                                                  'password2': 'pass1234sample', }, follow=True)

    def test_logout_page_url(self):
        response = self.client.get('/en/accounts/logout/')
        self.assertEqual(response.status_code, 200)

    def test_logout_page_reverse(self):
        response = self.client.get(reverse('account_logout'))
        self.assertEqual(response.status_code, 200)

    def test_logout_content(self):
        response = self.client.get(reverse('account_logout'))
        self.assertContains(response, 'Logout')

    def test_logout_template_used(self):
        response = self.client.get(reverse('account_logout'))
        self.assertTemplateUsed(response, 'account/logout.html')

    def test_logout(self):
        response = self.client.post('/en/accounts/logout/', follow=True)
        self.assertEqual(response.status_code, 200)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You have signed out.')

