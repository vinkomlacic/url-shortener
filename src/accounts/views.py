
from django.contrib.auth.views import LoginView, LogoutView


class URLShortenerLoginView(LoginView):
    template_name = 'accounts/login.html'


class URLShortenerLogoutView(LogoutView):
    pass
