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
from django.urls import resolve

from api.models import ExtendedEncoder, Challenge, SavedKata, Score


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


@csrf_exempt
def challenge(request):
    if request.user.is_anonymous:
        raise PermissionDenied()
    if config.CHALLENGE_ID < 0 \
            or not Challenge.objects.filter(id=config.CHALLENGE_ID).exists():
        raise Http404("No challenge found")
    challenge = Challenge.objects.get(pk=config.CHALLENGE_ID)
    if request.method == 'POST':
        if challenge.participants.filter(id=request.user.id).exists() is False:
            challenge.participants.add(request.user)
            challenge.save()
        if Score.objects.filter(user=request.user, challenge=challenge).exists() is False:
            score = Score(user=request.user, challenge=challenge, score=0)
            score.save()
    return JsonResponse(challenge.to_dict(), encoder=ExtendedEncoder)


def save_kata(request):
    if request.user.is_anonymous:
        raise PermissionDenied()
    savedKata = SavedKata.objects.filter(user=request.user, kata=request.user.current_kata,
                                         challenge_id=config.CHALLENGE_ID).first()
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    savedKata.saved_code = body['code']
    if 'test' in body:
        savedKata.saved_test = body['test']
    savedKata.save()
    return savedKata


def ranking(request):
    if request.user.is_anonymous:
        raise PermissionDenied()
    challenge = Challenge.objects.get(pk=config.CHALLENGE_ID)
    scores = Score.objects.filter(challenge=challenge).order_by('-score')
    score_list = []
    for i, score in enumerate(scores):
        dict = score.to_dict()
        dict['position'] = i + 1
        score_list.append(dict)
    return JsonResponse(score_list, encoder=ExtendedEncoder, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class CurrentKata(TemplateView):
    def next_kata(self, request):
        challenge = Challenge.objects.get(pk=config.CHALLENGE_ID)
        if challenge.startDate > timezone.now():
            raise PermissionDenied()
        if request.user.current_kata is None:
            raise PermissionDenied()
        if challenge.participants.filter(id=request.user.id).exists() is False:
            raise PermissionDenied()
        if Score.objects.filter(user=request.user, challenge=challenge).exists() is False:
            raise PermissionDenied()
        savedKata = SavedKata.objects.filter(user=request.user, kata=request.user.current_kata,
                                             challenge=challenge).first()
        if savedKata.solved is False:
            raise PermissionDenied()
        katas = challenge.katas.all()
        request.user.current_kata_index += 1
        request.user.save()
        if savedKata.to_dict()['is_last'] is True:
            score = Score.objects.filter(user=request.user, challenge=challenge).first()
            score.ended = True
            score.save()
            return JsonResponse({'is_end': True}, encoder=ExtendedEncoder)
        request.user.current_kata = katas[request.user.current_kata_index]
        request.user.save()
        savedKata = SavedKata(user=request.user, kata=request.user.current_kata,
                              challenge=challenge)
        savedKata.saved_code = request.user.current_kata.starter_code
        savedKata.saved_test = request.user.current_kata.test_example
        savedKata.solved = False
        savedKata.solved_at = None
        savedKata.save()
        kataDict = savedKata.to_dict()
        return JsonResponse(kataDict, encoder=ExtendedEncoder)

    def current_kata(self, request):
        if config.CHALLENGE_ID < 0 \
                or not Challenge.objects.filter(id=config.CHALLENGE_ID).exists():
            raise Http404("No challenge found")
        challenge = Challenge.objects.get(pk=config.CHALLENGE_ID)
        if challenge.startDate > timezone.now():
            raise PermissionDenied()
        if challenge.participants.filter(id=request.user.id).exists() is False:
            raise PermissionDenied()
        if Score.objects.filter(user=request.user, challenge=challenge).exists() is False:
            raise PermissionDenied()
        katas = challenge.katas.all()
        if request.user.current_kata is None or request.user.current_kata not in katas or SavedKata.objects.filter(
                user=request.user, kata=request.user.current_kata).count() == 0:
            request.user.current_kata = katas[0]
            request.user.current_kata_index = 0
            request.user.save()
            savedKata = SavedKata(user=request.user, kata=request.user.current_kata, challenge=challenge)
            savedKata.saved_code = request.user.current_kata.starter_code
            savedKata.saved_test = request.user.current_kata.test_example
            savedKata.solved = False
            savedKata.solved_at = None
            savedKata.save()
            kataDict = savedKata.to_dict()
            return JsonResponse(kataDict, encoder=ExtendedEncoder)
        else:
            savedKata = SavedKata.objects.filter(user=request.user, kata=request.user.current_kata, challenge=challenge).first()
            kataDict = savedKata.to_dict()
            return JsonResponse(kataDict, encoder=ExtendedEncoder)

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied()
        type = resolve(request.path_info).url_name
        if type == 'nextKata':
            return self.next_kata(request)
        elif type == 'currentKata':
            return self.current_kata(request)

    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied()
        if request.user.current_kata is None:
            raise PermissionDenied()
        savedKata = save_kata(request)
        return JsonResponse(savedKata.to_dict(), encoder=ExtendedEncoder)


@method_decorator(csrf_exempt, name='dispatch')
class CodeProcessor(TemplateView):

    def get_kata_index(self, challenge, kata):
        katas = challenge.katas.all()
        for i in range(len(katas)):
            if katas[i] == kata:
                return i
        return -1

    def test(self, request):
        savedKata = save_kata(request)
        runner = Runner("c", "codewars/systems-runner", savedKata.saved_code, savedKata.saved_test)
        output = runner.run()
        return JsonResponse(output, encoder=ExtendedEncoder)

    def run(self, request):
        savedKata = save_kata(request)
        challenge = Challenge.objects.get(pk=config.CHALLENGE_ID)
        if challenge.startDate > timezone.now():
            raise PermissionDenied()
        runner = Runner("c", "codewars/systems-runner", savedKata.saved_code, savedKata.kata.test_script)
        output = runner.run()
        if output.get("failed", 99) <= 0 and savedKata.solved is False:
            first_solved = None
            all_solved = SavedKata.objects.filter(kata=request.user.current_kata, solved=True, challenge=challenge)
            if all_solved.count() != 0:
                first_solved = all_solved.order_by('-solved_at').first()
            kata_weight = 1 + self.get_kata_index(challenge, request.user.current_kata) / 5
            calculated_score = 15000
            if first_solved is not None:
                calculated_score = (calculated_score - (timezone.now() - first_solved.solved_at).total_seconds() * 11) * kata_weight
            score = Score.objects.filter(user=request.user, challenge=challenge)
            if score.exists():
                my_score = score.first()
                my_score.score += calculated_score
                my_score.save()
            else:
                score = Score(user=request.user, challenge=savedKata.challenge, score=calculated_score)
                score.save()
            savedKata.solved = True
            savedKata.solved_at = timezone.now()
            savedKata.save()
        return JsonResponse(output, encoder=ExtendedEncoder)

    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied()
        if request.user.current_kata is None:
            raise PermissionDenied()
        type = resolve(request.path_info).url_name
        if type == 'test':
            return self.test(request)
        else:
            return self.run(request)
