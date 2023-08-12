from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView, ListView

from .models import URLMapping


class RedirectShortURL(RedirectView):
    """Redirects the shortened URL to its original counterpart."""

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.url_mapping = get_object_or_404(
            URLMapping, short_url=self.kwargs['short_url']
        )

    def get_redirect_url(self, *args, **kwargs):
        return self.url_mapping.url


class ShortURLList(ListView):
    model = URLMapping
    template_name = 'core/short_url_list.html'
    context_object_name = 'url_mappings'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(created_by=self.request.user)
        return queryset
