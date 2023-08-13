import random
import string

from django.conf import settings
from django.db import models
from django_lifecycle import (
    LifecycleModel, hook, BEFORE_CREATE, LifecycleModelMixin
)
from model_utils.models import TimeStampedModel


class URLMapping(LifecycleModelMixin, TimeStampedModel):
    url = models.URLField()
    short_url = models.CharField(max_length=10, db_index=True, blank=True,
                                 editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='url_mappings', editable=False
    )

    class Meta:
        ordering = ['-created']

    @hook(BEFORE_CREATE)
    def generate_short_url(self):
        charset = string.ascii_letters + string.digits
        short_url = ''.join(random.choice(charset) for _ in range(10))
        while URLMapping.objects.filter(short_url=short_url).exists():
            short_url = ''.join(random.choice(charset) for _ in range(10))

        self.short_url = short_url
