from django.contrib import messages
from django.urls import reverse_lazy


class ShortURLActionMixin:
    success_url = reverse_lazy('core:url_list')
    context_object_name = 'url_mapping'
    success_msg = 'Operation successfully completed!'

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)
