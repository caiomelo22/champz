from django.db import models
from WebApp.models.Position import Position
from WebApp.models.Participant import Participant
from WebApp.models.Team import Team
from WebApp.models.Nation import Nation


class Player(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    overall = models.IntegerField()
    pace = models.IntegerField(null=True)
    shooting = models.IntegerField(null=True)
    passing = models.IntegerField(null=True)
    dribbling = models.IntegerField(null=True)
    defending = models.IntegerField(null=True)
    physical = models.IntegerField(null=True)
    likes = models.IntegerField(null=True)
    value = models.IntegerField(null=True, blank=True)
    image_path = models.CharField(max_length=250, null=True)
    position = models.ForeignKey(Position, null=True, blank=True, on_delete=models.SET_NULL)
    specific_position = models.CharField(max_length=5, null=True)
    team_origin = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL,
                                       related_name="team_origin")
    team_participant = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL,
                                            related_name="team_participant")
    nation = models.ForeignKey(Nation, null=True, blank=True, on_delete=models.SET_NULL)

    @classmethod
    def create(cls, name, overall, position, team_origin, nation, image, spec_pos, likes):
        player = Player.objects.create(name=name, overall=overall, position=position, team_origin=team_origin, 
        nation=nation, image_path=image, specific_position=spec_pos, likes=likes)
        return player

    def buy_player(self, team, price):
        if self.team_participant:
            self.team_participant.participant.budget += self.value
            self.team_participant.participant.save()
            self.team_participant = None
            self.value = None
            self.save()

        if not team:
            return True

        participant = Participant.objects.get(id=team.participant.id)

        if participant.budget - price < 0:
            return False

        participant.budget -= price
        participant.save()

        self.value = price
        self.team_participant = team
        self.save()

        return True

    def __str__(self):
        return self.name