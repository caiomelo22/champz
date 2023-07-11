from rest_framework.response import Response
from rest_framework import viewsets
from WebApp.models.Nation import Nation
from WebApp.serializers.Nation import NationSerializer

class NationViewSet(viewsets.ModelViewSet):
    queryset = Nation.objects.all()
    serializer_class = NationSerializer

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        nation = Nation.create(data['name'], data['image_path'])
        nation = NationSerializer(nation, context={'request': request})
        return Response(nation.data)