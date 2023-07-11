from django.http import HttpResponseNotFound
from rest_framework.response import Response
from rest_framework import viewsets
from WebApp.models.Match import Match
from WebApp.models.Participant import Participant
from WebApp.models.Group import Group
from WebApp.serializers.Match import MatchSerializer

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        try:
            group = Group.objects.get(id=int(data['group']))
        except:
            return HttpResponseNotFound("Group not found")
        try:
            participant_1 = Participant.objects.get(id=int(data['participant_1']))
        except:
            return HttpResponseNotFound("Selected participant 1 not found")
        try:
            participant_2 = Participant.objects.get(id=int(data['participant_2']))
        except:
            return HttpResponseNotFound("Selected participant 2 not found")
        match = Match.create(group, participant_1, participant_2)
        match = MatchSerializer(match, context={'request': request})
        return Response(match.data)

    def update(self, request, *args, **kwargs):
        data = dict(request.data)
        instance = self.queryset.get(id=data['id'])
        instance.goals_participant_1 = data['goals_participant_1']
        instance.goals_participant_2 = data['goals_participant_2']
        instance.save()
        return Response(MatchSerializer(instance).data)