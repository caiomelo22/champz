from django.http import HttpResponseNotFound, HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from WebApp.models.Player import Player
from WebApp.models.Participant import Participant
from WebApp.models.Position import Position
from WebApp.models.Team import Team
from WebApp.models.Nation import Nation
from WebApp.models.League import League
from WebApp.serializers.Player import PlayerSerializer
from WebApp.services import get_players_db, get_players_by_position_algorithm, get_players_by_position_string
import openpyxl

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all().order_by('-overall', '-pace')
    serializer_class = PlayerSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['position', 'team_participant', 'team_origin']

    def cut_player_quantity(self, position):
        n_participants = len(Participant.objects.all())
        if position.name == 'Goalkeepers':
            return get_players_by_position_algorithm(position.id, 1.5*n_participants)
        elif position.name == 'Center Backs':
            return get_players_by_position_algorithm(position.id, 3*n_participants)
        elif position.name == 'Full Backs':
            return get_players_by_position_algorithm(position.id, 3*n_participants)
        elif position.name == 'Defensive Midfielders':
            return get_players_by_position_algorithm(position.id, 3*n_participants)
        elif position.name == 'Ofensive Midfielders':
            return get_players_by_position_algorithm(position.id, 1.5*n_participants)
        elif position.name == 'Wingers':
            return get_players_by_position_algorithm(position.id, 2.5*n_participants)
        elif position.name == 'Attackers':
            return get_players_by_position_algorithm(position.id, 2*n_participants)

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        try:
            position = Position.objects.get(id=int(data['position']))
        except:
            return HttpResponseNotFound("Position not found")
        try:
            team_origin = Team.objects.get(id=int(data['team_origin']))
        except:
            return HttpResponseNotFound("Team not found")
        try:
            nation = Nation.objects.get(id=int(data['nation']))
        except:
            return HttpResponseNotFound("Nation not found")
        player = Player.create(data['name'], int(
            data['overall']), position, team_origin, nation, data['image_path'], data['specific_position'])
        player = PlayerSerializer(player, context={'request': request})
        return Response(player.data)

    def list(self, request, *args, **kwargs):
        players = list(Player.objects.all().order_by('-overall'))
        if 'team_participant' in request._request.__dict__['environ']['QUERY_STRING']:
            team_participant = request._request.__dict__['environ']['QUERY_STRING'].split('=')[1]
            players = [player for player in players if str(player.team_participant_id)==team_participant]
            players.sort(key=lambda item: (item.overall, item.pace), reverse=True)
        if 'position' in request._request.__dict__['environ']['QUERY_STRING']:
            position = request._request.__dict__['environ']['QUERY_STRING'].split('=')[1]
            try:
                position_obj = Position.objects.get(id=position)
            except:
                return HttpResponseNotFound("Position not found")
            players = self.cut_player_quantity(position_obj)
        
        return Response(PlayerSerializer(players, many=True).data)

class BuyPlayerView(APIView):
    def post(self, request, id):
        player = Player.objects.filter(id=id)
        if len(player) == 0:
            return HttpResponseNotFound("There are no players with the given id.")
        else:
            player = player[0]

        data = dict(request.data)

        team = None
        price = None
        if data.get('team_participant') is not None:
            team = Team.objects.filter(id=int(data['team_participant']))
            if len(team) == 0:
                return HttpResponseNotFound("There are no teams with the given id.")
            else:
                team = team[0]
            price = int(data['value'])

        result = player.buy_player(team, price)

        if result:
            return Response(PlayerSerializer(player).data)
        else:
            return HttpResponseBadRequest("The budget of {} is not enough to buy {}".format(data['team_participant'], player))

class TransfersView(APIView):
    def get(self, request):
        file = open("transfers.txt", "w", encoding="utf-8")
        leagues = League.objects.all().order_by('name')
        team_participant = None
        for league in leagues:
            team_participant = None
            strBuilder = ""
            strBuilder += ("LEAGUE: {}\n".format(league.name.upper()))
            teams = Team.objects.filter(league=league.id).order_by('name')
            for team in teams:
                strBuilder += ("\tTEAM: {}\n".format(team.name.replace('ş', 's').upper()))
                players = Player.objects.filter(team_origin=team.id).order_by(
                    '-team_participant', '-overall')
                for player in players:
                    if player.team_participant != None and player.team_participant != team:
                        team_participant = player.team_participant
                        strBuilder += ("\t\tTO {}: {} - {}\n".format(
                            team_participant.name.upper(), player.overall, player.name.upper()))
            strBuilder += ('--------------------------------------------------------------------------\n')
            if team_participant is not None:
                file.write(strBuilder)

        file.close()

        return Response()

class ChampzPlayersView(APIView):
    def get(self, request):
        positions = list(Position.objects.all())
        wb = openpyxl.Workbook()
        for i,position in enumerate(positions):
            wb.create_sheet(index = i , title = position.name)
        n_participants = len(list(Participant.objects.all()))
        wb.active = 0
        get_players_by_position_string(wb.active, positions[0], 1.5*n_participants)
        wb.active = 1
        get_players_by_position_string(wb.active, positions[1], 3*n_participants)
        wb.active = 2
        get_players_by_position_string(wb.active, positions[2], 3*n_participants)
        wb.active = 3
        get_players_by_position_string(wb.active, positions[3], 3*n_participants)
        wb.active = 4
        get_players_by_position_string(wb.active, positions[4], 1.5*n_participants)
        wb.active = 5
        get_players_by_position_string(wb.active, positions[5], 2.5*n_participants)
        wb.active = 6
        get_players_by_position_string(wb.active, positions[6], 2*n_participants)

        wb.save("players.xlsx") 

        return Response()

class UpdatePlayerDatabaseView(APIView):
    def post(self, request):
        get_players_db()
        return Response()

