from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', include('github_auth.urls.login')),
    path('auth/github/callback', include('github_auth.urls.callback')),
    path('logout', include('github_auth.urls.logout')),

    path('api/me', views.me, name='me'),
    path('api/challenge', views.challenge, name='challenge'),
    path('api/test/', views.CodeProcessor.as_view(), name='challenge'),
    path('api/kata/current/', views.CurrentKata.as_view(), name='currentKata'),

    path('', views.home, name='index'),
    re_path(r'^.*$', views.check_auth, name='index'),

]