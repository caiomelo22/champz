from django.db import models
import math
from random import shuffle
from WebApp.models.Participant import Participant
from WebApp.models.Match import Match


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    participants = models.ManyToManyField(Participant)
    previous_stage = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

    @classmethod
    def create(cls, name):
        group = Group.objects.create(name=name)
        return group

    def add_participant(self, participant):
        self.participants.add(participant)
        self.save()

    def create_matches(self):
        participants_list = list(self.participants.all())
        shuffle(participants_list)

        matches = []

        half = math.floor(len(participants_list)/2)
        first_half = participants_list[:half]
        second_half = participants_list[half:]

        for i in range(len(participants_list)):
            for j in range(len(first_half)):
                matches.append(Match.create(self, first_half[j], list(reversed(second_half))[j]))
            first_half.append(second_half.pop(0))
            second_half.append(first_half.pop(0))

        self.matches = matches

        return matches

    def set_game_stats(self, stats_participant, goals_for, goals_against):
        stats_participant['GF'] += goals_for
        stats_participant['GA'] += goals_against
        stats_participant['GD'] += stats_participant['GF'] - stats_participant['GA']
        return stats_participant
    
    def set_record_stats(self, stats, winner, loser):
        stats[winner]['P'] += 3
        stats[winner]['W'] += 1
        stats[loser]['L'] += 1
        return stats

    def set_draw_stats(self, stats_participant, participant):
        stats_participant['P'] += 1
        stats_participant['D'] += 1
        return stats_participant

    def get_group_table(self):
        participants = list(self.participants.all())
        stats = dict((p,{'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0}) for p in participants)

        matches = list(Match.objects.filter(group=self))
        for match in matches:
            if match.goals_participant_1 != None and match.goals_participant_2 != None:
                stats[match.participant_1] = self.set_game_stats(stats[match.participant_1], match.goals_participant_1, match.goals_participant_2)
                stats[match.participant_2] = self.set_game_stats(stats[match.participant_2], match.goals_participant_2, match.goals_participant_1)
                if match.goals_participant_1 > match.goals_participant_2:
                    stats = self.set_record_stats(stats, match.participant_1, match.participant_2)
                elif match.goals_participant_2 > match.goals_participant_1:
                    stats = self.set_record_stats(stats, match.participant_2, match.participant_1)
                else:
                    stats[match.participant_1] = self.set_draw_stats(stats[match.participant_1], match.participant_1)
                    stats[match.participant_2] = self.set_draw_stats(stats[match.participant_2], match.participant_2)

        stats_list = list(stats.items())
        stats_list = sorted(stats_list, key=lambda x: (x[1]['P'], x[1]['W'], x[1]['GD'], x[1]['GF']), reverse=True)
        return stats_list

    def export_matches(self):
        file = open("matches.txt", "w")

        file.write('MATCHES: \n\n')

        strBuilder = ""
        strBuilder += '{}\n'.format(self.name.upper())
        for match in self.matches:
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

    def __str__(self):
        return self.name