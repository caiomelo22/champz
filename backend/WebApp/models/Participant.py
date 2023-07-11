from django.db import models

class Participant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    budget = models.IntegerField()

    @classmethod
    def create(cls, name, budget, team):
        participant = Participant.objects.create(name=name, budget=budget)
        team.participant = participant
        team.save()
        return participant

    def __str__(self):
        return self.name