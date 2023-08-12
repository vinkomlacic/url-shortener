from django.urls import path

from .views import RedirectShortURL, ShortURLList

app_name = 'core'

urlpatterns = [
    path('urls', ShortURLList.as_view(), name='url_list'),
    path('<str:short_url>', RedirectShortURL.as_view(), name='redirect'),
]
