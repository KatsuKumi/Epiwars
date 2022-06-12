import json

from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from api.models import Challenge, SavedKata, ExtendedEncoder, Kata
from django.contrib.admin.views.decorators import staff_member_required
from constance import config


def admin_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_anonymous or not request.user.is_staff:
            raise PermissionDenied()
        else:
            return view_func(request, *args, **kwargs)

    return wrap


@admin_only
def panel(request):
    return render(request, 'index.html')


@admin_only
def panel_redirect(request):
    return redirect('/panel/')


@method_decorator([csrf_exempt, staff_member_required], name='dispatch')
class ChallengeListView(TemplateView):

    def get(self, request, *args, **kwargs):
        challenges = Challenge.objects.all().values()
        challenge_list = [challenge for challenge in challenges]
        for challenge in challenge_list:
            if config.CHALLENGE_ID == challenge['id']:
                challenge['active'] = True
            else:
                challenge['active'] = False
        return JsonResponse(challenge_list, encoder=ExtendedEncoder, safe=False)

    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        challenge = Challenge.objects.create(**body)
        return JsonResponse(challenge.to_dict(), encoder=ExtendedEncoder)


@method_decorator([csrf_exempt, staff_member_required], name='dispatch')
class ChallengeView(TemplateView):

    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        challenge = Challenge.objects.get(pk=id)
        return JsonResponse(challenge.to_dict(), encoder=ExtendedEncoder)

    def delete(self, request, *args, **kwargs):
        id = kwargs['pk']
        challenge = Challenge.objects.get(pk=id)
        challenge.delete()
        return JsonResponse({})

    def put(self, request, *args, **kwargs):
        id = kwargs['pk']
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        challenge = Challenge.objects.get(pk=id)
        challenge.name = body['name']
        challenge.description = body['description']
        challenge.startDate = body['startDate']
        challenge.save()
        return JsonResponse(challenge.to_dict(), encoder=ExtendedEncoder)


@csrf_exempt
@staff_member_required
def list_challenge_katas(request, pk):
    challenge = Challenge.objects.get(pk=pk)
    katas = challenge.katas.all().values()
    kata_list = [kata for kata in katas]
    return JsonResponse(kata_list, encoder=ExtendedEncoder, safe=False)


@method_decorator([csrf_exempt, staff_member_required], name='dispatch')
class KataListView(TemplateView):

    def get(self, request, *args, **kwargs):
        katas = Kata.objects.all().values()
        kata_list = [kata for kata in katas]
        return JsonResponse(kata_list, encoder=ExtendedEncoder, safe=False)

    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        kata = Kata.objects.create(**body)
        return JsonResponse(kata.to_dict(), encoder=ExtendedEncoder)


@method_decorator([csrf_exempt, staff_member_required], name='dispatch')
class KataView(TemplateView):

    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        kata = Kata.objects.get(pk=id)
        return JsonResponse(kata.to_dict(), encoder=ExtendedEncoder)

    def delete(self, request, *args, **kwargs):
        id = kwargs['pk']
        kata = Kata.objects.get(pk=id)
        kata.delete()
        return JsonResponse({})

    def put(self, request, *args, **kwargs):
        id = kwargs['pk']
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        kata = Kata.objects.get(pk=id)
        kata.name = body['name']
        kata.description = body['description']
        kata.starter_code = body['starter_code']
        kata.test_script = body['test_script']
        kata.test_example = body['test_example']
        kata.save()
        return JsonResponse(kata.to_dict(), encoder=ExtendedEncoder)


@method_decorator([csrf_exempt, staff_member_required], name='dispatch')
class ChallengeKataView(TemplateView):

    def post(self, request, *args, **kwargs):
        challenge_id = kwargs['pk']
        kata_id = kwargs['pk2']
        body = json.loads(request.body.decode('utf-8'))
        direction = body['direction']
        challenge = Challenge.objects.get(pk=challenge_id)
        kata = Kata.objects.get(pk=kata_id)
        katas = list(challenge.katas.all())
        if kata not in katas:
            raise PermissionDenied()
        if direction == 'up':
            index = katas.index(kata)
            if index > 0:
                katas.remove(kata)
                katas.insert(index - 1, kata)
                challenge.katas.clear()
                challenge.katas.add(*katas)
        elif direction == 'down':
            index = katas.index(kata)
            print(index)
            if index < len(katas) - 1:
                katas.remove(kata)
                katas.insert(index + 1, kata)
                challenge.katas.clear()
                challenge.katas.add(*katas)
        return list_challenge_katas(request, challenge_id)

    def put(self, request, *args, **kwargs):
        challenge_id = kwargs['pk']
        kata_id = kwargs['pk2']
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        challenge = Challenge.objects.get(pk=challenge_id)
        kata = Kata.objects.get(pk=kata_id)
        katas = list(challenge.katas.all())
        position = body['position']
        if position == "start":
            katas.insert(0, kata)
            challenge.katas.clear()
            challenge.katas.add(*katas)
        elif position == "end":
            katas.append(kata)
            challenge.katas.clear()
            challenge.katas.add(*katas)
        return list_challenge_katas(request, challenge_id)

    def delete(self, request, *args, **kwargs):
        challenge_id = kwargs['pk']
        kata_id = kwargs['pk2']
        challenge = Challenge.objects.get(pk=challenge_id)
        kata = Kata.objects.get(pk=kata_id)
        challenge.katas.remove(kata)
        return list_challenge_katas(request, challenge_id)


@csrf_exempt
@staff_member_required
def active_challenge(request):
    if request.method != 'POST':
        raise PermissionDenied()
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    challenge_id = body['challenge']
    if challenge_id is None or challenge_id == "" or Challenge.objects.filter(pk=challenge_id).count() == 0:
        raise PermissionDenied()
    challenge = Challenge.objects.get(pk=challenge_id)
    if challenge.katas.count() == 0:
        return JsonResponse({'error': 'No katas in challenge'}, status=400)
    config.CHALLENGE_ID = challenge_id
    return JsonResponse({})
