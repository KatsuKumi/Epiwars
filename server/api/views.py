from datetime import timedelta

from django.core.exceptions import PermissionDenied
from django.forms import model_to_dict
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import json
from django.core import serializers
from django.utils import timezone
from constance import config
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from api.runner import Runner

from api.models import ExtendedEncoder, Challenge, SavedKata


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
    return JsonResponse(request.user.to_dict(), encoder=ExtendedEncoder)


def challenge(request):
    if request.user.is_anonymous:
        raise PermissionDenied()
    challenge = Challenge.objects.get(pk=config.CHALLENGE_ID)
    return JsonResponse(challenge.to_dict(), encoder=ExtendedEncoder)


@method_decorator(csrf_exempt, name='dispatch')
class CurrentKata(TemplateView):

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied()
        challenge = Challenge.objects.get(pk=config.CHALLENGE_ID)
        if challenge.startDate > timezone.now():
            raise PermissionDenied()
        katas = challenge.katas.all()
        if request.user.current_kata is None or request.user.current_kata not in katas or SavedKata.objects.filter(
                user=request.user, kata=request.user.current_kata).count() == 0:
            request.user.current_kata = katas[0]
            request.user.save()
            savedKata = SavedKata(user=request.user, kata=request.user.current_kata)
            savedKata.saved_code = request.user.current_kata.starter_code
            savedKata.saved_test = request.user.current_kata.test_example
            savedKata.save()
            return JsonResponse(savedKata.to_dict(), encoder=ExtendedEncoder)
        else:
            savedKata = SavedKata.objects.filter(user=request.user, kata=request.user.current_kata).first()
            return JsonResponse(savedKata.to_dict(), encoder=ExtendedEncoder)

    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied()
        if request.user.current_kata is None:
            raise PermissionDenied()
        savedKata = SavedKata.objects.filter(user=request.user, kata=request.user.current_kata).first()
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        savedKata.saved_code = body['code']
        savedKata.saved_test = body['test']
        savedKata.save()
        return JsonResponse(savedKata.to_dict(), encoder=ExtendedEncoder)


@method_decorator(csrf_exempt, name='dispatch')
class CodeProcessor(TemplateView):

    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied()
        if request.user.current_kata is None:
            raise PermissionDenied()
        savedKata = SavedKata.objects.filter(user=request.user, kata=request.user.current_kata).first()
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        savedKata.saved_code = body['code']
        savedKata.saved_test = body['test']
        savedKata.save()
        runner = Runner("c", "codewars/systems-runner", savedKata.saved_code, savedKata.saved_test)
        output = runner.run()
        return JsonResponse(output, encoder=ExtendedEncoder)


