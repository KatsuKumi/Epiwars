from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

urlpatterns = [
    path('', LogoutView.as_view(next_page=(getattr(settings,'LOGOUT_REDIRECT_URL','/') or '/')))
]
