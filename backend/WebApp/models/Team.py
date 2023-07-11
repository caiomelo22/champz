from django.db import models
from WebApp.models.League import League
from WebApp.models.Participant import Participant

class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    league = models.ForeignKey(League, null=True, blank=True, on_delete=models.CASCADE)
    participant = models.OneToOneField(Participant, null=True, blank=True, on_delete=models.SET_NULL)
    image_path = models.CharField(max_length=250, null=True)

    @classmethod
    def create(cls, name, league, image):
        team = Team.objects.create(name=name, league=league, image_path=image)
        return team

    def __str__(self):
        return self.name