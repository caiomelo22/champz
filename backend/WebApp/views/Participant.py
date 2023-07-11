from django.http import HttpResponseNotFound, HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from WebApp.models.Participant import Participant
from WebApp.models.Team import Team
from WebApp.models.Player import Player
from WebApp.serializers.Participant import ParticipantSerializer
from WebApp.services import write_players_sheet
import openpyxl

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        try:
            team = Team.objects.get(id=int(data['team']))
        except:
            return HttpResponseNotFound("Selected team not found")
        if team.participant != None:
            return HttpResponseBadRequest("The chosen team has already been assigned to another participant.")
        participant = Participant.create(
            data['name'], int(data['budget']), team)
        participant = ParticipantSerializer(
            participant, context={'request': request})
        return Response(participant.data)

    def update(self, request, *args, **kwargs):
        try:
            instance = Participant.objects.get(id=kwargs.get('pk'))
        except:
            return HttpResponseNotFound("Participant not found")
        data = dict(request.data)
        team = data.get('team')
        if team != None:
            old_team = Team.objects.filter(participant=instance.id)
            new_team = Team.objects.filter(id=int(team))
            if len(new_team)>0 and (new_team[0].participant != None and new_team[0].participant.id != instance.id):
                    return HttpResponseBadRequest("The chosen team has already been assigned to another participant.")
            elif len(new_team) > 0:
                new_team = new_team[0]
            else:
                return HttpResponseBadRequest("The chosen team does not exist.")

            if len(old_team) > 0:
                old_team = old_team[0]

                players_old_team = Player.objects.filter(team_participant=old_team.id)
                for player in players_old_team:
                    player.team_participant = new_team
                    player.save()
                
                if team != old_team.id:
                    old_team.participant = None
       
            new_team.participant = instance
            if old_team:
                old_team.save()
            new_team.save()
            del data['team']

        serializer = self.serializer_class(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = Participant.objects.get(id=kwargs.get('pk'))
        except:
            return HttpResponseNotFound("Participant not found")
        team = Team.objects.get(participant=instance.id)
        players = Player.objects.filter(team_participant=team.id)
        for player in players:
            player.team_participant = None
            player.value = None
            player.save()
        instance.delete()
        return Response(ParticipantSerializer(instance).data)

class ParticipantsTeamsView(APIView):
    def get(self, request):
        participants = Participant.objects.all()
        wb = openpyxl.Workbook()
        for i,participant in enumerate(participants):
            participant_team = Team.objects.get(participant=participant)
            participant_players = Player.objects.filter(team_participant=participant_team).order_by('position', 'specific_position', '-overall')
            wb.create_sheet(index = i , title = "{}({})".format(participant.name, participant_team.name))
            wb.active = i
            write_players_sheet(wb.active, participant_players)

        wb.save("teams.xlsx") 

        return Response()