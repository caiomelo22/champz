from django.http import HttpResponseNotFound
from rest_framework.response import Response
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from WebApp.models.Team import Team
from WebApp.models.League import League
from WebApp.serializers.Team import TeamSerializer
from WebApp.services import update_teams_leagues

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all().order_by('name')
    serializer_class = TeamSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['league']

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        try:
            league = League.objects.get(id=int(data['league']))
        except:
            return HttpResponseNotFound("League not found")
        team = Team.create(data['name'], league, data['image_path'])
        team = TeamSerializer(team, context={'request': request})
        return Response(team.data)

class UpdateTeamsLeaguesDatabaseView(APIView):
    def post(self, request):
        update_teams_leagues()
        return Response()