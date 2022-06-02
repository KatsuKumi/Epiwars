from django.urls import path

from github_auth.views import GithubOAuthCallbackView

urlpatterns = [
    path('', GithubOAuthCallbackView.as_view(),name='callback'),
]
