from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from api import views
from panel import views as panel_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', include('github_auth.urls.login')),
    path('auth/github/callback', include('github_auth.urls.callback')),
    path('logout', include('github_auth.urls.logout')),

    path('api/me', views.me, name='me'),
    path('api/ranking', views.ranking, name='rank'),
    path('api/katas/', panel_views.KataListView.as_view(), name='list_katas'),
    path('api/katas/<int:pk>/',panel_views. KataView.as_view(), name='challenge'),
    path('api/challenges/active', panel_views.active_challenge, name='active_challenge'),
    path('api/challenges/', panel_views.ChallengeListView.as_view(), name='test'),
    path('api/challenges/<int:pk>/', panel_views.ChallengeView.as_view(), name='challenge'),
    path('api/challenges/<int:pk>/katas/', panel_views.list_challenge_katas, name='challenge'),
    path('api/challenges/<int:pk>/katas/<int:pk2>/', panel_views.ChallengeKataView.as_view(), name='challenge'),
    path('api/challenge', views.challenge, name='challenge'),
    path('api/test/', views.CodeProcessor.as_view(), name='test'),
    path('api/test/submit/', views.CodeProcessor.as_view(), name='submit'),
    path('api/kata/current/', views.CurrentKata.as_view(), name='currentKata'),
    path('api/kata/next/', views.CurrentKata.as_view(), name='nextKata'),

    re_path(r'^panel$', panel_views.panel_redirect, name='panel'),
    re_path(r'^panel/.*$', panel_views.panel, name='panel'),
    path('', views.home, name='index'),
    re_path(r'^.*$', views.check_auth, name='index'),
]