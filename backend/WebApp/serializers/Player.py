from WebApp.models.Player import Player
from rest_framework import serializers
from .Team import TeamSerializer
from .Position import PositionSerializer
from .Nation import NationSerializer


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    team_participant = TeamSerializer()
    position = PositionSerializer()
    nation = NationSerializer()
    team_origin = TeamSerializer()
    class Meta:
        model = Player
        fields = ['id', 'name', 'overall', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physical', 'likes',
                  'value', 'position', 'team_origin', 'team_participant', 'nation', 'image_path', 'specific_position']