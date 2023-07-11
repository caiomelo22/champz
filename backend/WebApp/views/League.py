from rest_framework.response import Response
from rest_framework import viewsets
from WebApp.models.League import League
from WebApp.serializers.League import LeagueSerializer

class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        league = League.create(data['name'])
        league = LeagueSerializer(league, context={'request': request})
        return Response(league.data)