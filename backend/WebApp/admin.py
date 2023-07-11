from django.contrib import admin

# Register your models here.
from WebApp.models.Position import Position
from WebApp.models.Participant import Participant
from WebApp.models.Team import Team
from WebApp.models.Nation import Nation
from WebApp.models.League import League
from WebApp.models.Group import Group
from WebApp.models.Match import Match
from WebApp.models.Player import Player

admin.site.register(Nation)
admin.site.register(League)
admin.site.register(Team)
admin.site.register(Participant)
admin.site.register(Position)
admin.site.register(Player)
admin.site.register(Group)
admin.site.register(Match)

