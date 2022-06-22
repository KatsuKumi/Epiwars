from django.core.management.base import BaseCommand, CommandError
from api.models import Challenge, SavedKata, User, Score
from constance import config

class Command(BaseCommand):
    help = 'Reset all saved katas and users'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        challenges = Challenge.objects.filter(id=config.CHALLENGE_ID)
        if challenges.count() == 0:
            print("Invalid challenge id %d" % config.CHALLENGE_ID)
            return
        answer = input("Are you sure you want to reset the challenge %d ? (Y/N) " % config.CHALLENGE_ID)
        if answer != "Y" and answer != 'y':
            return
        challenge = challenges.first()
        for kata in list(challenge.katas.all()):
            savedKatas = SavedKata.objects.filter(kata=kata)
            if savedKatas.count() > 0:
                print("Deleting %d saved katas for kata %s" % (savedKatas.count(), kata.name))
                savedKatas.delete()
        users = User.objects.all()
        for user in users:
            user.current_kata = None
            user.current_kata_index = 0
            user.save()
        scores = Score.objects.filter(challenge=challenge)
        if scores.count() > 0:
            print("Deleting %d scores for challenge %s" % (scores.count(), challenge.name))
            scores.delete()
        print("Reset done")

