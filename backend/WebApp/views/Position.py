from rest_framework.response import Response
from rest_framework import viewsets
from WebApp.models.Position import Position
from WebApp.serializers.Position import PositionSerializer

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        position = Position.create(data['name'])
        position = PositionSerializer(position, context={'request': request})
        return Response(position.data)