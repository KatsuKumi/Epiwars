from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model


class User(AbstractUser):
    avatar = models.CharField(max_length=200, default="")

    # add additional fields in here

    def __str__(self):
        return self.username


class ExtendedEncoder(DjangoJSONEncoder):

    def default(self, o):

        if isinstance(o, Model):
            return model_to_dict(o)

        return super().default(o)