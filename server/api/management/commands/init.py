from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from api.models import Challenge, Kata
from constance import config
from django.utils.timezone import make_aware


def get_date_input(prompt):
    print(prompt)
    while True:
        try:
            line = input()
        except EOFError:
            break
        try:
            return datetime.strptime(line, "%d/%m/%Y %H:%M:%S")
        except ValueError:
            print("Invalid date format, must be YYYY-MM-DD HH:MM:SS")


def get_multiline_input(prompt):
    print(prompt)
    contents = []
    while True:
        try:
            line = input("")
        except EOFError:
            break
        contents.append(line)
    return "\n".join(contents)


class Command(BaseCommand):
    help = 'Create a new challenge'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        challenge_name = input("Challenge name: ")
        if challenge_name == "":
            raise CommandError("Invalid challenge name")
        challenge_start = get_date_input("Challenge start date: (format DD/MM/YYYY HH:MM:SS)")
        challenge_description = input("Challenge description: ")
        if challenge_description == "":
            raise CommandError("Invalid challenge description")
        challenge = Challenge(name=challenge_name, startDate=make_aware(challenge_start), description=challenge_description)
        challenge.save()
        print("Please add katas to the challenge")
        print("To add a kata, type 'add <kata_name>'")
        print("To finish, type 'finish'")
        print("To cancel, type 'cancel'")
        print("To see the list of katas, type 'list'")
        while True:
            cmd = input("> ")
            if cmd == "finish":
                break
            elif cmd == "cancel":
                print("Challenge %s deleted" % challenge_name)
                break
            elif cmd == "list":
                print("Katas:")
                for kata in challenge.katas.all():
                    print("  %s" % kata.name)
            elif cmd.startswith("add "):
                kata_name = cmd[4:]
                print("Please enter the following information for kata \"%s\", press Ctrl-D or Ctrl-Z ( windows ) to "
                      "save it." % kata_name)
                kata_description = get_multiline_input("Description (support Markdown): ")
                kata_starter_code = get_multiline_input("Starter code: ")
                kata_test_example = get_multiline_input("Test example: ")
                kata_test_script = get_multiline_input("Test script: ")
                kata = Kata(name=kata_name, test_script="\n".join(kata_test_script), test_example="\n".join(kata_test_example), description="\n".join(kata_description), starter_code="\n".join(kata_starter_code))
                kata.save()
                challenge.katas.add(kata)
                print("Kata %s added" % kata_name)
            else:
                print("Invalid command")
        print("Challenge %s finished" % challenge_name)
        default = input("Set as default challenge? (Y/N) ")
        if default == "Y" or default == "y":
            config.CHALLENGE_ID = challenge.id
            print("Default challenge set to %d" % challenge.id)
        print("Challenge %s created" % challenge_name)



