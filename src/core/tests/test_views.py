from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from django.test import TestCase, RequestFactory
from django.urls import reverse

from accounts.models import User
from core.models import URLMapping
from core.views import RedirectShortURL, ShortURLList


class CoreViewsTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.factory = RequestFactory()

        cls.redirect_url_pattern = 'core:redirect'
        cls.url_list_url = reverse('core:url_list')
        cls.url_create_url = reverse('core:url_create')
        cls.url_update_url_pattern = 'core:url_update'
        cls.url_delete_url_pattern = 'core:url_delete'

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = User.objects.create_user(username='test', password='test')

    def test_redirect_short_url_setup_raises_404(self):
        """If a short URL does not exist, the view should raise 404."""
        kwargs = {'short_url': 'test'}
        url = reverse(self.redirect_url_pattern, kwargs=kwargs)
        request = self.factory.get(url)
        request.user = AnonymousUser()

        view = RedirectShortURL()
        with self.assertRaises(Http404):
            view.setup(request, **kwargs)

    def test_redirect_short_url(self):
        """
        If the short URL exists, the view should return a redirect to the
        original URL.
        """
        target_url = 'https://example.org'
        url_mapping = URLMapping.objects.create(
            url=target_url, created_by=self.user
        )

        # Setup request
        request_kwargs = {'short_url': url_mapping.short_url}
        request_url = reverse(self.redirect_url_pattern, kwargs=request_kwargs)
        request = self.factory.get(request_url)

        response = RedirectShortURL.as_view()(request, **request_kwargs)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, target_url)

    def test_short_url_list_no_objects(self):
        """
        If there are no objects in the database, the returned queryset
        should be empty.
        """
        url = self.url_list_url
        request = self.factory.get(url)
        request.user = self.user

        view = ShortURLList()
        view.setup(request)
        queryset = view.get_queryset()

        self.assertFalse(queryset.exists())

    def test_short_url_list_with_objects(self):
        """If there are some objects in the DB, the URL should return them."""
        n_objects = 3
        for _ in range(n_objects):
            URLMapping.objects.create(
                url='https://example.org', created_by=self.user
            )

        url = self.url_list_url
        request = self.factory.get(url)
        request.user = self.user

        view = ShortURLList()
        view.setup(request)
        queryset = view.get_queryset()

        self.assertEqual(queryset.count(), n_objects)

    def test_short_url_list_filters_by_current_user(self):
        """
        If there are URLs in the DB, the list view should only returns
        those related to the current user.
        """
        n_objects = 3
        for _ in range(n_objects):
            self.user.url_mappings.create(url='https://example.org')
        other_user = User.objects.create_user(
            username='other_user', password='test'
        )
        other_user.url_mappings.create(url='https://example.org')

        url = self.url_list_url
        request = self.factory.get(url)
        request.user = self.user

        view = ShortURLList()
        view.setup(request)
        queryset = view.get_queryset()

        self.assertEqual(queryset.count(), n_objects)

    def test_short_url_list_filters_by_search_query(self):
        """
        If there are objects in the database and a search query is specified,
        the queryset should be limited to the URL mappings that mathc the URL
        in the query (case-insensitive contains operator).
        """
        self.user.url_mappings.create(url='https://example.org')
        self.user.url_mappings.create(url='https://EXAMPLE.ORG')
        self.user.url_mappings.create(url='https://test.org')

        query = 'example.org'
        expected_matches = 2  # the first and second URL should match

        url = self.url_list_url + f'?q={query}'
        request = self.factory.get(url)
        request.user = self.user

        view = ShortURLList()
        view.setup(request)
        queryset = view.get_queryset()

        self.assertEqual(queryset.count(), expected_matches)

    def test_short_url_create(self):
        """
        If URL is valid, a new URL mapping should be created and the view
        should redirect to the URL list.
        """
        # Using test client in this test because messages framework requires
        # installing the messages middleware
        login_success = self.client.login(username='test', password='test')
        self.assertTrue(login_success)

        response = self.client.post(
            self.url_create_url, data={'url': 'https://example.org'}
        )

        self.assertRedirects(response, expected_url=self.url_list_url)
        self.assertTrue(URLMapping.objects.exists())

    def test_short_url_update(self):
        """
        If URL is valid, the URL mapping should be updated and the view
        should redirect to the URL list.
        """
        # Using test client in this test because messages framework requires
        # installing the messages middleware
        login_success = self.client.login(username='test', password='test')
        self.assertTrue(login_success)
        url_mapping = self.user.url_mappings.create(url='https://example.org')

        request_url = reverse(
            self.url_update_url_pattern, args=(url_mapping.pk,)
        )
        response = self.client.post(
            request_url, data={'url': 'https://example2.org'}
        )

        self.assertRedirects(response, expected_url=self.url_list_url)
        url_mapping.refresh_from_db()
        self.assertEqual(url_mapping.url, 'https://example2.org')

    def test_short_url_delete(self):
        """
        If successful, the call to delete view should delete the URL
        mapping instance and the view should redirect to the URL list.
        """
        # Using test client in this test because messages framework requires
        # installing the messages middleware
        login_success = self.client.login(username='test', password='test')
        self.assertTrue(login_success)
        url_mapping = self.user.url_mappings.create(url='https://example.org')

        request_url = reverse(
            self.url_delete_url_pattern, args=(url_mapping.pk,)
        )
        response = self.client.post(request_url)

        self.assertRedirects(response, expected_url=self.url_list_url)
        with self.assertRaises(URLMapping.DoesNotExist):
            url_mapping.refresh_from_db()
