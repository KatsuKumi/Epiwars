from datetime import timedelta

from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import json
from django.core import serializers
from django.utils import timezone

from api.models import ExtendedEncoder


def home(request):
    if not request.user.is_anonymous:
        return redirect('/home')
    return render(request, 'index.html')


def check_auth(request):
    if request.user.is_anonymous:
        return redirect('/')
    if not request.user.email:
        return redirect('/?error=notek')
    return render(request, 'index.html')


def me(request):
    if request.user.is_anonymous:
        raise PermissionDenied()
    return JsonResponse({
        "username": request.user.username, "email": request.user.email, "avatar": request.user.avatar
    }, encoder=ExtendedEncoder)


def challenge(request):
    if request.user.is_anonymous:
        raise PermissionDenied()
    return JsonResponse({"startDate": timezone.now() + timedelta(seconds=5), "name": "Epiwars 0.1"},
                        encoder=ExtendedEncoder)

