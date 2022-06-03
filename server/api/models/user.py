from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model


class SavedKata(models.Model):
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Saved Kata'
        verbose_name_plural = 'Saved Katas'

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    kata = models.ForeignKey('Kata', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    saved_code = models.TextField()
    saved_test = models.TextField()

    def to_dict(self):
        return {
            'user': self.user.username,
            'kata': self.kata.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'saved_code': self.saved_code,
            'saved_test': self.saved_test,
            'description': self.kata.description,
        }

    def __str__(self):
        return self.user.username + ' - ' + self.kata.name


class User(AbstractUser):
    avatar = models.CharField(max_length=200, default="")
    current_kata = models.ForeignKey('Kata', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username

    def to_dict(self):
        return model_to_dict(self, exclude=['password', 'groups', 'user_permissions'])


class ExtendedEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if callable(getattr(obj, 'to_dict', None)):
            return obj.to_dict()
        elif isinstance(obj, Model):
            return model_to_dict(obj)
        return super().default(obj)