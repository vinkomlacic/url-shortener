from django.urls import path

from .views import URLShortenerLoginView, URLShortenerLogoutView

app_name = 'accounts'

urlpatterns = [
    path('login', URLShortenerLoginView.as_view(), name='login'),
    path('logout', URLShortenerLogoutView.as_view(), name='logout'),
]
