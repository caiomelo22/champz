from django.http import HttpResponseNotFound, HttpResponseBadRequest, JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from WebApp.models.Group import Group
from WebApp.models.Match import Match
from WebApp.models.Participant import Participant
from WebApp.serializers.Group import GroupSerializer
from WebApp.serializers.Participant import ParticipantSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        group = Group.create(data['group'])
        group = GroupSerializer(group, context={'request': request})
        return Response(group.data)

class GetGroupTableView(APIView):
    def get(self, request, id):
        group = Group.objects.filter(id=id)
        if len(group) == 0:
            return HttpResponseNotFound("There are no groups with the given id.")
        else:
            group = group[0]

        table = group.get_group_table()
        new_table = []

        [new_table.append((ParticipantSerializer(p[0]).data, p[1])) for p in table]
        return JsonResponse(new_table, safe=False)

class GetGroupStageView(APIView):
    def post(self, request):
        replace = request.data['replace']
        group = Group.objects.filter(name='Group 1')
        if len(group) > 0 and not replace:
            group[0].matches = list(Match.objects.filter(group=group[0]))
            return Response(GroupSerializer(group[0]).data)
        elif len(group) > 0:
            group[0].delete()
        
        participants = Participant.objects.all()
        group = Group.create('Group 1')
        for participant in participants:
            group.add_participant(participant)
        
        group.create_matches()

        group.export_matches()

        return Response(GroupSerializer(group).data)

class GetWildcardKnockoutRoundView(APIView):
    def post(self, request):
        replace = request.data['replace']
        matches_wildcard = []

        old_stage = Group.objects.filter(name='Wildcard')
        if len(old_stage) > 0 and not replace:
            old_stage[0].matches = list(Match.objects.filter(group=old_stage[0]))
            return Response(GroupSerializer(old_stage[0]).data)
        elif len(old_stage) > 0:
            old_stage = old_stage[0]
            old_stage.delete()

        groups = list(Group.objects.filter(name='Group 1'))

        if len(groups) == 1:
            table_wildcard = groups[0].get_group_table()[2:6]
            wildcard = Group.create('Wildcard')
            wildcard.previous_stage = groups[0]

            for participant in table_wildcard:
                wildcard.add_participant(participant[0])

            matches_wildcard.append(Match.create(wildcard, table_wildcard[0][0], table_wildcard[3][0]))
            matches_wildcard.append(Match.create(wildcard, table_wildcard[1][0], table_wildcard[2][0]))

            wildcard.matches = matches_wildcard
            
            wildcard.save()
        else:
            return HttpResponseBadRequest("Number of groups does not allow the generation of a knockout round.")

        return Response(GroupSerializer(wildcard).data)


class GetSemiFinalsRoundView(APIView):
    def check_position_group_stage(self, participant, group_stage):
        for i, position in enumerate(group_stage):
            if position[0] == participant:
                return i
        return -1

    def get_group_winners(self, group, participants, group_stage):
        qualified = []
        try:
            group = Group.objects.get(name=group)
        except:
            return HttpResponseNotFound("Group not found")
        for participant in participants:
            if participant[1]['P'] == 3:
                qualified.append(participant[0])
            elif participant[1]['P'] == 1:
                opponent = group.find_match_group_participant_opponent(participant[0])
                position_participant = self.check_position_group_stage(participant[0], group_stage)
                position_opponent = self.check_position_group_stage(opponent, group_stage)
                if position_participant < position_opponent:
                    qualified.append(participant[0])

            if len(qualified) == 2:
                break

        return qualified

    def post(self, request):
        replace = request.data['replace']
        matches_semis = []

        old_stage = Group.objects.filter(name='Semis')
        if len(old_stage) > 0 and not replace:
            old_stage[0].matches = list(Match.objects.filter(group=old_stage[0]))
            return Response(GroupSerializer(old_stage[0]).data)
        elif len(old_stage) > 0:
            old_stage = old_stage[0]
            old_stage.delete()

        try:
            group_stage = Group.objects.get(name='Group 1')
        except:
            return HttpResponseNotFound("Group stage not found")
        table_group_stage = group_stage.get_group_table()
 
        try:
            wildcard_stage = Group.objects.get(name='Wildcard')
        except:
            return HttpResponseNotFound("Wildcard stage not found")
        table_wildcard = wildcard_stage.get_group_table()
        semis = Group.create('Semis')
        semis.previous_stage = wildcard_stage

        wildcard_winners = self.get_group_winners('Wildcard', table_wildcard, table_group_stage)

        semis.add_participant(table_group_stage[0][0])
        semis.add_participant(table_group_stage[1][0])
        semis.add_participant(wildcard_winners[0])
        semis.add_participant(wildcard_winners[1])

        wc1_position = self.check_position_group_stage(wildcard_winners[0], table_group_stage)
        wc2_position = self.check_position_group_stage(wildcard_winners[1], table_group_stage)

        if wc1_position < wc2_position:
            matches_semis.append(Match.create(semis, table_group_stage[0][0], wildcard_winners[1]))
            matches_semis.append(Match.create(semis,  wildcard_winners[1], table_group_stage[0][0]))
            matches_semis.append(Match.create(semis, table_group_stage[1][0], wildcard_winners[0]))
            matches_semis.append(Match.create(semis, wildcard_winners[0], table_group_stage[1][0]))
        else:
            matches_semis.append(Match.create(semis, table_group_stage[0][0], wildcard_winners[0]))
            matches_semis.append(Match.create(semis, wildcard_winners[0], table_group_stage[0][0]))
            matches_semis.append(Match.create(semis, table_group_stage[1][0], wildcard_winners[1]))
            matches_semis.append(Match.create(semis, wildcard_winners[1], table_group_stage[1][0]))

        semis.matches = matches_semis

        semis.save()

        return Response(GroupSerializer(semis).data)


class GetFinalView(APIView):
    def check_position_group_stage(self, participant, group_stage):
        for i, position in enumerate(group_stage):
            if position[0] == participant:
                return i
        return -1
        
    def post(self, request):
        replace = request.data['replace']
        
        old_stage = Group.objects.filter(name='Final')
        if len(old_stage) > 0 and not replace:
            old_stage[0].matches = list(Match.objects.filter(group=old_stage[0]))
            return Response(GroupSerializer(old_stage[0]).data)
        elif len(old_stage) > 0:
            old_stage = old_stage[0]
            old_stage.delete()

        semis = Group.objects.get(name='Semis')

        participants = semis.get_group_table()
        qualified = list()

        qualified.append(participants[0][0])
        qualified.append(participants[1][0])

        matches = []
            
        final = Group.create('Final')
        final.previous_stage = semis

        for participant in qualified:
            final.add_participant(participant)

        matches.append(Match.create(final, qualified[0], qualified[1]))

        final.matches = matches

        final.save()

        return Response(GroupSerializer(final).data)