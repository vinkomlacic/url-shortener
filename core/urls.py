from django.urls import path

from .views import RedirectShortURL, ShortURLList, ShortURLCreate

app_name = 'core'

urlpatterns = [
    path('urls', ShortURLList.as_view(), name='url_list'),
    path('urls/create', ShortURLCreate.as_view(), name='url_create'),
    path('<str:short_url>', RedirectShortURL.as_view(), name='redirect'),
]
