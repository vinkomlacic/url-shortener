from django.contrib import admin
from .models import URLMapping


@admin.register(URLMapping)
class URLMappingAdmin(admin.ModelAdmin):
    list_display = ('url', 'short_url',)
