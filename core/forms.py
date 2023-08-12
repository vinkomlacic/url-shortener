from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from .models import URLMapping


class URLMappingCreateForm(forms.ModelForm):

    class Meta:
        model = URLMapping
        fields = ['url']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        if self.user.is_demo_account:
            url_limit = settings.URL_SHORTENER_DEMO_ACCOUNT_MAX_URLS
            is_limit_exceeded = self.user.url_mappings.count() >= url_limit
            if is_limit_exceeded:
                err = f'You have exceeded the limit of allowed shortened URLs '
                err += f'for the demo user. Please delete some of the old '
                err += f'URLs to be able to add new ones. '
                err += f'URL limit: {url_limit}. '
                raise ValidationError(err, code='demo_user_limit_exceeded')

    def save(self, *args, **kwargs):
        is_unsaved = self.instance.pk is None
        if is_unsaved:
            self.instance.created_by = self.user

        return super().save(*args, **kwargs)
