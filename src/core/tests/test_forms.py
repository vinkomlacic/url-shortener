from django.test import TestCase

from accounts.models import User
from core.forms import URLMappingCreateForm


class CoreFormsTest(TestCase):

    def test_url_mapping_form_validates_demo_user_url_limit(self):
        """
        The demo users have a limit on the amount of URLs they can create. If
        it's over the limit, the form should not validate.
        """
        user = User.objects.create_user(username='test', password='test',
                                        is_demo_account=True)
        # If this setting is set to 0 any attempt at creating a new
        # URLMapping for a demo user should fail.
        with self.settings(URL_SHORTENER_DEMO_ACCOUNT_MAX_URLS=0):
            form = URLMappingCreateForm(
                user=user, data={'url': 'https://example.org'}
            )

            self.assertFalse(form.is_valid())
            self.assertEqual(
                form.non_field_errors().data[0].code,
                'demo_user_limit_exceeded'
            )
