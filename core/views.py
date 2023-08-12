from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import (
    RedirectView, ListView, CreateView, UpdateView, DeleteView
)

from .models import URLMapping
from .forms import URLMappingCreateForm
from .viewmixins import ShortURLActionMixin


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
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(created_by=self.request.user)
        queryset = self._filter_queryset_by_search_query(queryset)
        return queryset

    def _filter_queryset_by_search_query(self, queryset):
        query = self.request.GET.get('q', None)
        if not query:
            return queryset

        queryset = queryset.filter(url__icontains=query)
        return queryset


class ShortURLCreate(LoginRequiredMixin, ShortURLActionMixin, CreateView):
    model = URLMapping
    template_name = 'core/short_url_form.html'
    success_msg = 'Short URL successfully created!'
    form_class = URLMappingCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class ShortURLUpdate(LoginRequiredMixin, ShortURLActionMixin, UpdateView):
    model = URLMapping
    template_name = 'core/short_url_form.html'
    success_msg = 'Short URL successfully updated!'
    fields = ['url']
    pk_url_kwarg = 'pk_url'


class ShortURLDelete(LoginRequiredMixin, ShortURLActionMixin, DeleteView):
    model = URLMapping
    template_name = 'core/short_url_delete.html'
    success_msg = 'Short URL successfully deleted!'
    pk_url_kwarg = 'pk_url'
