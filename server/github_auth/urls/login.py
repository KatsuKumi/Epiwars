from django.conf import settings
from django.urls import path

from github_auth.views import GithubOAuthLoginView

urlpatterns = [
    path('', GithubOAuthLoginView.as_view()),
]
