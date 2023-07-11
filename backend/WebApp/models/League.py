from django.db import models

class League(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    @classmethod
    def create(cls, name):
        league = League.objects.create(name=name)
        return league

    def __str__(self):
        return self.name