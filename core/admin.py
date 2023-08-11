from django.contrib import admin
from .models import URLMapping


@admin.register(URLMapping)
class DefaultAdmin(admin.ModelAdmin):
    pass
