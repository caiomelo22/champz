from WebApp.models.Team import Team
from WebApp.models.Participant import Participant
from .League import LeagueSerializer
from rest_framework import serializers

class TeamSerializer(serializers.HyperlinkedModelSerializer):
    league = LeagueSerializer()
    participant = serializers.PrimaryKeyRelatedField(queryset=Participant.objects.all())
    class Meta:
        model = Team
        fields = ['id', 'name', 'league', 'image_path', 'participant']