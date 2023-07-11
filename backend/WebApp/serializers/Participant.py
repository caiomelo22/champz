from WebApp.models.Participant import Participant
from rest_framework import serializers
from .Team import TeamSerializer

class ParticipantSerializer(serializers.HyperlinkedModelSerializer):
    team = TeamSerializer(read_only = True)
    team_loading_att = serializers.SerializerMethodField('is_team_loading')

    def is_team_loading(self, obj):
        return False
        
    class Meta:
        model = Participant
        fields = ['id', 'name', 'budget', 'team', 'team_loading_att']