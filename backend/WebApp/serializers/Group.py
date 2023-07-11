from WebApp.models.Group import Group
from rest_framework import serializers
from .Participant import ParticipantSerializer
from .Match import MatchSerializer

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    participants = ParticipantSerializer(read_only=True, many=True)
    matches = MatchSerializer(read_only = True, many=True)
    class Meta:
        model = Group
        fields = ['id', 'name', 'participants', 'matches']