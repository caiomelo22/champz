from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from WebApp.models.Player import Player
from WebApp.models.Participant import Participant
from WebApp.models.Team import Team
from WebApp.models.Group import Group
from WebApp.models.Match import Match

class EndChampzView(APIView):
    def post(self, request):
        file = open("champz.txt", "w", encoding="utf-8")
        participants = Participant.objects.all()
        file.write("TEAMS: \n\n")
        for participant in participants:
            strBuilder = ""
            strBuilder += 'TEAM {}'.format(participant.name.upper())
            team_participant = Team.objects.get(participant=participant)
            strBuilder += '({})\n'.format(team_participant.name.upper())
            players_participant = Player.objects.filter(team_participant=team_participant).order_by('-overall')
            for player in players_participant:
                strBuilder += '\t{} - {} - ${}\n'.format(player.name, player.overall, player.value)
            strBuilder += '\n'
            file.write(strBuilder)

        groups = list(Group.objects.all())
        group_stage = [g for g in groups if 'Group' in g.name]

        for index, group in enumerate(group_stage):
            table = group.get_group_table()

            file.write('GROUP {} TABLE\n\n'.format(index+1))
            file.write('TEAM\t\tP\tW\tD\tL\tGF\tGA\tGD\n')
            for el in table:
                participant = Participant.objects.get(name=el[0])
                if len(participant.name) > 8:
                    file.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(participant.name, el[1]['P'], el[1]['W'], el[1]['D'], el[1]['L'], el[1]['GF'], el[1]['GA'], el[1]['GD']))
                else:
                    file.write('{}\t\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(participant.name, el[1]['P'], el[1]['W'], el[1]['D'], el[1]['L'], el[1]['GF'], el[1]['GA'], el[1]['GD']))
            file.write('\n')


        file.write('MATCHES: \n\n')

        for group in groups:
            strBuilder = ""
            strBuilder += '{}\n'.format(group.name.upper())
            matches = Match.objects.filter(group=group)
            for match in matches:
                participant_1 = match.participant_1.name
                participant_2 = match.participant_2.name
                goals_1 = match.goals_participant_1
                if goals_1 is None:
                    goals_1 = ''
                goals_2 = match.goals_participant_2
                if goals_2 is None:
                    goals_2 = ''
                strBuilder += '\t{} {} x {} {}\n'.format(participant_1, goals_1, goals_2, participant_2)
            strBuilder += '\n'
            file.write(strBuilder)

        file.close()

        return Response()
