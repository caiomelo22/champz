from WebApp.models.Nation import Nation
from rest_framework import serializers

class NationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Nation
        fields = ['id', 'name', 'image_path']