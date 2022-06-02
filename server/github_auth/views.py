from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect
from django.views.generic.base import View

from .classes import OAuthClient
from .utils import get_user_data, get_user_emails
from . import signals


class GithubOAuthMixin:
    client_id = None
    secret = None
    callback_url = None
    scopes = None

    def get_client_id(self):
        return self.client_id or settings.GITHUB_OAUTH_CLIENT_ID

    def get_secret(self):
        return self.secret or settings.GITHUB_OAUTH_SECRET

    def get_callback_url(self):
        url = self.callback_url or settings.GITHUB_OAUTH_CALLBACK_URL
        return self.request.build_absolute_uri(url)

    def get_scopes(self):
        return self.scopes or getattr(settings, 'GITHUB_OAUTH_SCOPES', [])

    def get_client(self):
        kwargs = {
            'client_id': self.get_client_id(),
            'secret': self.get_secret(),
            'callback_url': self.get_callback_url(),
            'scopes': self.get_scopes()
        }
        return OAuthClient(self.request, **kwargs)


class GithubOAuthLoginView(GithubOAuthMixin, View):

    def get(self, request, *args, **kwargs):
        client = self.get_client()
        return redirect(client.get_redirect_url())


class GithubOAuthCallbackView(GithubOAuthMixin, View):
    backend = None

    def dispatch(self, *args, **kwargs):
        self.token = self.get_token()
        self.data = get_user_data(self.token)
        self.emails = get_user_emails(self.token)
        self.email = ""
        for email in self.emails:
            if "@epitech.eu" in email["email"]:
                self.email = email["email"]
        self.user = self.get_user(self.data['login'], self.email)
        self.save_token(self.user, self.token)
        signals.user_login.send(sender=None, request=self.user, token=self.token, emails=self.emails)
        return super().dispatch(*args, **kwargs)

    def get_backend(self):
        if self.backend:
            return backend
        if hasattr(settings, 'GITHUB_OAUTH_BACKEND'):
            return settings.GITHUB_OAUTH_BACKEND

    def get_token(self):
        client = self.get_client()
        return client.get_token(self.request.GET['code'])

    def get_user_model(self):
        return get_user_model()

    def get_user(self, login, email):
        user_model = self.get_user_model()
        defaults = {user_model.USERNAME_FIELD: login, "email": email}
        kwargs = dict(id=self.data['id'])
        user, _ = user_model.objects.update_or_create(defaults, **kwargs)
        return user

    def save_token(self, user,token):
        pass

    def get_redirect_url(self):
        if 'next' in self.request.GET:
            return redirect(self.request.GET['next'])
        return settings.LOGIN_REDIRECT_URL if settings.LOGIN_REDIRECT_URL else '/'

    def get(self, request, *args, **kwargs):
        backend = self.get_backend()
        kwargs = {'backend': backend} if backend else {}
        login(self.request, self.user, **kwargs)
        return redirect(self.get_redirect_url())
