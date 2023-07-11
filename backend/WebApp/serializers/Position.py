from WebApp.models.Position import Position
from rest_framework import serializers

class PositionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'name']