from WebApp.models.League import League
from rest_framework import serializers

class LeagueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = League
        fields = ['id', 'name']