from django.contrib import admin

from .models import User


@admin.register(User)
class DefaultAdmin(admin.ModelAdmin):
    pass
