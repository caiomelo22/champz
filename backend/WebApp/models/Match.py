from django.db import models
from WebApp.models.Participant import Participant

class Match(models.Model):
    id = models.AutoField(primary_key=True)
    goals_participant_1 = models.IntegerField(null=True)
    goals_participant_2 = models.IntegerField(null=True)
    group = models.ForeignKey('WebApp.Group', on_delete=models.CASCADE)
    participant_1 = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="participant_1")
    participant_2 = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="participant_2")

    @classmethod
    def create(cls, group, participant_1, participant_2):
        match = Match.objects.create(group=group, participant_1=participant_1, participant_2=participant_2)
        return match

    def register_score(self, goals_participant_1, goals_participant_2):
        self.goals_participant_1 = goals_participant_1
        self.goals_participant_2 = goals_participant_2
        self.save()

    def __str__(self):
        return "{} {} x {} {}".format(self.participant_1, self.goals_participant_1, self.goals_participant_2, self.participant_2)
