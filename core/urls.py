from django.urls import path
from django.views.generic import RedirectView

from .views import RedirectShortURL, ShortURLList, ShortURLCreate, \
    ShortURLUpdate

app_name = 'core'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='core:url_list'), name='home'),
    path('urls', ShortURLList.as_view(), name='url_list'),
    path('urls/create', ShortURLCreate.as_view(), name='url_create'),
    path(
        'urls/<int:pk_url>/update',
        ShortURLUpdate.as_view(),
        name='url_update'
    ),
    path('<str:short_url>', RedirectShortURL.as_view(), name='redirect'),
]
