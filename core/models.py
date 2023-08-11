import random
import string

from django.db import models
from django_lifecycle import LifecycleModel, hook, BEFORE_CREATE


class URLMapping(LifecycleModel):
    url = models.URLField()
    short_url = models.CharField(max_length=10, db_index=True)

    @hook(BEFORE_CREATE)
    def generate_short_url(self):
        charset = string.ascii_letters + string.digits
        short_url = ''.join(random.choice(charset) for _ in range(10))
        while self.objects.filter(short_url=short_url).exists():
            short_url = ''.join(random.choice(charset) for _ in range(10))

        self.short_url = short_url
