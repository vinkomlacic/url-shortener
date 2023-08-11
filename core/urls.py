from django.urls import path

from .views import RedirectShortURL

app_name = 'core'

urlpatterns = [
    path('<str:short_url>', RedirectShortURL.as_view(), name='redirect'),
]
