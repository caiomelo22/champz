from WebApp.models.Match import Match
from rest_framework import serializers
from .Participant import ParticipantSerializer

class MatchSerializer(serializers.HyperlinkedModelSerializer):
    participant_1 = ParticipantSerializer()
    participant_2 = ParticipantSerializer()
    class Meta:
        model = Match
        fields = ['id', 'goals_participant_1', 'goals_participant_2', 'participant_1', 'participant_2']
