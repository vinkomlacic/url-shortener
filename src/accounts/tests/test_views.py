from django.test import TestCase
from django.urls import reverse

from accounts.models import User


class AccountsViewsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.login_url = reverse('accounts:login')
        cls.logout_url = reverse('accounts:logout')
        cls.home_url = reverse('core:home')

    def test_login(self):
        """
        Logging in with valid credentials should redirect to the home page.
        """
        test_data = {'username': 'test', 'password': 'password'}
        User.objects.create_user(**test_data)

        response = self.client.post(self.login_url, data=test_data)
        self.assertRedirects(
            response, expected_url=self.home_url,
            # Home also redirects to URL list, it doesn't return 200
            target_status_code=302,
        )

    def test_login_invalid_credentials(self):
        """
        Logging in with invalid credentials re-renders the page with errors.
        """
        test_data = {'username': 'test', 'password': 'password'}

        response = self.client.post(self.login_url, data=test_data)
        # 200 is returned for invalid form, not 302
        self.assertEqual(response.status_code, 200)
