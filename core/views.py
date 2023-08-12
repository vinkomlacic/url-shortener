from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import RedirectView, ListView, CreateView

from .models import URLMapping


class RedirectShortURL(RedirectView):
    """
    Redirects the shortened URL to its original counterpart.

    This is a public view.
    """

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.url_mapping = get_object_or_404(
            URLMapping, short_url=self.kwargs['short_url']
        )

    def get_redirect_url(self, *args, **kwargs):
        return self.url_mapping.url


class ShortURLList(LoginRequiredMixin, ListView):
    model = URLMapping
    template_name = 'core/short_url_list.html'
    context_object_name = 'url_mappings'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(created_by=self.request.user)
        return queryset


class ShortURLCreate(LoginRequiredMixin, CreateView):
    model = URLMapping
    template_name = 'core/short_url_create.html'
    fields = ['url']
    success_url = reverse_lazy('core:url_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
