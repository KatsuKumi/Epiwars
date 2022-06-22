from django.db import models
from sortedm2m.fields import SortedManyToManyField


class Kata(models.Model):
    name = models.CharField(max_length=200)
    test_script = models.TextField()
    test_example = models.TextField()
    description = models.TextField()
    starter_code = models.TextField()

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'name': self.name,
            'test_script': self.test_script,
            'test_example': self.test_example,
            'description': self.description,
            'starter_code': self.starter_code
        }


class Challenge(models.Model):
    startDate = models.DateTimeField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    first_kata = models.ForeignKey(Kata, on_delete=models.CASCADE, related_name='first_kata', null=True)
    katas = SortedManyToManyField(Kata)
    participants = models.ManyToManyField('api.User', related_name='challenges')

    def to_dict(self):
        return {
            'startDate': self.startDate,
            'name': self.name,
            'description': self.description
        }

    def __str__(self):
        return self.name