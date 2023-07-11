from random import randint

from django.http import HttpResponseBadRequest
from django.test import TestCase

from rest_framework.utils import json
from WebApp.models.Position import Position
from WebApp.models.Participant import Participant
from WebApp.models.Team import Team
from WebApp.models.Nation import Nation
from WebApp.models.League import League
from WebApp.models.Group import Group
from WebApp.models.Match import Match
from WebApp.models.Player import Player


class WebAppTestCase(TestCase):
    # def test_methods(self):
    #     england = Nation.create('England')
    #     belgium = Nation.create('Belgium')
    #     nations = Nation.objects.all()
    #     self.assertEqual(len(nations), 2)
    #
    #     league = League.create('Premier League')
    #     leagues = League.objects.all()
    #     self.assertEqual(len(leagues), 1)
    #
    #     city = Team.create('Manchester City', league)
    #     united = Team.create('Manchester United', league)
    #     liverpool = Team.create('Liverpool', league)
    #     chelsea = Team.create('Chelsea', league)
    #     teams = Team.objects.all()
    #     self.assertEqual(len(teams), 4)
    #
    #     position = Position.create('Attacking Midfielder')
    #     positions = Position.objects.all()
    #     self.assertEqual(len(positions), 1)
    #
    #     kdb = Player.create('Kevin De Bruyne', 91, position, city, belgium)
    #     players = Player.objects.all()
    #     self.assertEqual(len(players), 1)
    #
    #     caio = Participant.create('Caio', 100, city)
    #     joao = Participant.create('João', 100, united)
    #     jorge = Participant.create('Jorge', 100, liverpool)
    #     rodrigo = Participant.create('Rodrigo', 100, chelsea)
    #     participants = Participant.objects.all()
    #     self.assertEqual(len(participants), 4)
    #
    #     kdb.buy_player(liverpool, 22)
    #     self.assertEqual(jorge.budget, 78)
    #     self.assertEqual(kdb.team_participant, liverpool)
    #
    #     kdb.buy_player(city, 22)
    #     self.assertEqual(caio.budget, 78)
    #     self.assertEqual(jorge.budget, 100)
    #     self.assertEqual(kdb.team_participant, city)
    #
    #     result = kdb.buy_player(united, 101)
    #     self.assertEqual(joao.budget, 100)
    #     self.assertEqual(kdb.team_participant, city)
    #     self.assertEqual(result, False)
    #
    #     result = kdb.buy_player(None, 0)
    #     self.assertEqual(caio.budget, 100)
    #     self.assertEqual(kdb.team_participant, None)
    #     self.assertEqual(result, True)
    #
    #     group_1 = Group.create('1')
    #     group_1.add_participant(city)
    #     group_1.add_participant(united)
    #     group_1.add_participant(liverpool)
    #     group_1.add_participant(chelsea)
    #     groups = Group.objects.all()
    #     self.assertEqual(len(groups), 1)
    #     group_1.create_matches()
    #     matches = Match.objects.all()
    #
    #     # print("\nMATCHES:")
    #     for match in matches:
    #         match.registerScore(randint(0,3),randint(0,3))
    #         # print(match)
    #
    #     # print('\nGROUP TABLE:')
    #     # for participant in group_1.get_group_table():
    #         # print(participant)
    #
    #     self.assertEqual(len(matches), 6)
    #
    # def get_id_from_href(self, link):
    #     start = link.find("player/")
    #     end = link.find('/', start + 8)
    #     return link[start + 7:end]
    #
    # # Verifica se alguma versão antiga daquele jogador já existe na lista e se existir, devolverá o index dele
    # def get_player_index(self, obj, position):
    #     players = list(Player.objects.filter(position=position))
    #     for player in players:
    #         if obj.name == player.name and int(obj.id) > int(player.id):
    #             return player.id
    #         elif obj.name == player.name:
    #             return -1
    #     return -2
    #
    # def test_get_futhead_data(self):
    #     positions = {'Goalkeepers': 'GK', 'Center Backs': 'CB', 'Full Backs': 'RB,LB', 'Defensive Midfielders': 'CDM,CM',
    #                 'Ofensive Midfielders': 'CAM', 'Wingers': 'LW,LF,LM,RF,RW,RM', 'Attackers': 'ST,CF'}
    #
    #     base_url = "https://www.futbin.com/20/players?version=gold_rare&position="
    #
    #     # CRIANDO O LOOP PARA PASSAR POR TODAS AS POSICOES
    #     for name, positions in positions.items():
    #         position = Position.create(name)
    #
    #         # PEGANDO OS JOGADORES DO FUTBIN
    #
    #         for pagina in range(1):
    #             url = base_url + positions
    #
    #             url = url + '&page=' + str(pagina)
    #
    #             #print(url)
    #
    #             url = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    #             client = uReq(url)
    #             html = client.read()
    #             client.close()
    #             page_soup = soup(html, "html.parser")
    #             players_1 = page_soup.findAll("tr", {"class": "player_tr_1"})
    #             players_2 = page_soup.findAll("tr", {"class": "player_tr_2"})
    #
    #             # PEGANDO DADOS DOS JOGADORES
    #
    #             cont = 0
    #             lista = 1
    #
    #             while cont < len(players_1):
    #                 if lista == 1:
    #                     jogador = players_1[cont]
    #                 else:
    #                     jogador = players_2[cont]
    #
    #                 tds = jogador.findAll('td')
    #
    #
    #                 data = tds[0].findAll('a')
    #
    #                 player = Player(position=position)
    #
    #                 player.name = ''.join(data[0].findAll(text=True))
    #
    #                 player.id = self.get_id_from_href(data[0]['href'])
    #
    #                 league = data[3]['data-original-title']
    #                 query = League.objects.filter(name=league)
    #                 if len(query) == 0:
    #                     league = League.create(league)
    #                 else:
    #                     league = query[0]
    #                 player.league = league
    #
    #                 team = data[1]['data-original-title']
    #                 query = Team.objects.filter(name=team)
    #                 if len(query) == 0:
    #                     team = Team.create(team, league)
    #                 else:
    #                     team = query[0]
    #                 player.team_origin = team
    #
    #                 nation = data[2]['data-original-title']
    #                 query = Nation.objects.filter(name=nation)
    #                 if len(query) == 0:
    #                     nation = Nation.create(nation)
    #                 else:
    #                     nation = query[0]
    #                 player.nation = nation
    #
    #                 player.overall = ''.join(tds[1].findAll(text=True))
    #
    #                 # dados['posicao'] = ''.join(tds[2].findAll(text=True))
    #                 # dados['preco'] = ''.join(tds[4].findAll(text=True))
    #
    #                 # rates = tds[7].findAll('span')
    #                 # dados['attack_rate'] = ''.join(rates[0].findAll(text=True))
    #                 # dados['defense_rate'] = ''.join(rates[1].findAll(text=True))
    #
    #                 # dados['stats'] = dict()
    #                 player.pace = ''.join(tds[8].findAll(text=True))
    #                 player.shooting = ''.join(tds[9].findAll(text=True))
    #                 player.passing = ''.join(tds[10].findAll(text=True))
    #                 player.dribbling = ''.join(tds[11].findAll(text=True))
    #                 player.defending = ''.join(tds[12].findAll(text=True))
    #                 player.physical = ''.join(tds[13].findAll(text=True))
    #
    #                 # dados['altura'] = ''.join(tds[14].div.findAll(text=True))
    #
    #                 index = self.get_player_index(player, position)
    #
    #                 if index >= 0:
    #                     player_to_delete = Player.objects.get(id=index)
    #                     player_to_delete.delete()
    #                     player.save()
    #                 elif index == -2:
    #                     player.save()
    #                 else:
    #                     pass
    #
    #                 if lista == 1:
    #                     lista = 2
    #                 else:
    #                     lista = 1
    #                     cont += 1
    #         # all_players_from_position = list(Player.objects.filter(position=position))
    #         # print(position.name, len(all_players_from_position))
    #
    #     print('\nPOSITIONS:', len(Position.objects.all()))
    #     print('LEAGUES:', len(League.objects.all()))
    #     print('NATION:', len(Nation.objects.all()))
    #     print('PLAYERS:', len(Player.objects.all()))
    #
    #     print('\nJOGADORES DO BARCELONA:')
    #     barcelona = Team.objects.get(name='FC Barcelona')
    #     for player in list(Player.objects.filter(team_origin=barcelona)):
    #         print('PLAYER: ', player.name, '::: NATION:', player.nation, '::: OVERALL:', player.overall)
    #
    #     self.assertEqual(1,1)

    def test_views(self):
        england = self.client.post("/api/nation/", {"name": "England"})
        belgium = self.client.post('/api/nation/', {'name': 'Belgium'})
        nations = Nation.objects.all()
        self.assertEqual(len(nations), 2)

        league = self.client.post('/api/league/', {'name': 'Premier League'})
        leagues = League.objects.all()
        self.assertEqual(len(leagues), 1)

        city = self.client.post('/api/team/', {'name': 'Manchester City', 'league': league.data['id']})
        united = self.client.post('/api/team/', {'name': 'Manchester United', 'league': league.data['id']})
        liverpool = self.client.post('/api/team/', {'name': 'Liverpool', 'league': league.data['id']})
        chelsea = self.client.post('/api/team/', {'name': 'Chelsea', 'league': league.data['id']})
        teams = list(Team.objects.all())
        self.assertEqual(len(teams), 4)

        position = self.client.post('/api/position/', {'name': 'Attacking Midfielder'})
        positions = Position.objects.all()
        self.assertEqual(len(positions), 1)

        kdb = self.client.post('/api/player/', {'name': 'Kevin De Bruyne', 'overall': 91, 'position': position.data['id'],
                                                'team_origin': city.data['id'], 'nation': belgium.data['id']})
        players = Player.objects.all()
        self.assertEqual(len(players), 1)

        caio = self.client.post('/api/participant/', {'name': 'Caio', 'budget': 100, 'team': city.data['id']})
        joao =self.client.post('/api/participant/', {'name': 'João', 'budget': 100, 'team': united.data['id']})
        jorge = self.client.post('/api/participant/', {'name': 'Jorge', 'budget': 100, 'team': liverpool.data['id']})
        rodrigo = self.client.post('/api/participant/', {'name': 'Rodrigo', 'budget': 100, 'team': chelsea.data['id']})
        participants = Participant.objects.all()
        self.assertEqual(len(participants), 4)

        result = self.client.post('/api/buy/' + str(kdb.data['id']), {'team': liverpool.data['id'], 'price': 22})
        self.assertEqual(Participant.objects.get(id=jorge.data['id']).budget, 78)
        self.assertEqual(Player.objects.get(id=kdb.data['id']).team_participant.id, liverpool.data['id'])

        result = self.client.post('/api/buy/' + str(kdb.data['id']), {'team': city.data['id'], 'price': 22})
        self.assertEqual(Participant.objects.get(id=caio.data['id']).budget, 78)
        self.assertEqual(Participant.objects.get(id=jorge.data['id']).budget, 100)
        self.assertEqual(Player.objects.get(id=kdb.data['id']).team_participant.id, city.data['id'])

        result = self.client.post('/api/buy/' + str(kdb.data['id']), {'team': united.data['id'], 'price': 101})
        self.assertEqual(Participant.objects.get(id=joao.data['id']).budget, 100)
        self.assertEqual(Player.objects.get(id=kdb.data['id']).team_participant.id, city.data['id'])
        self.assertEqual(result.status_code, HttpResponseBadRequest.status_code)

        result = self.client.post('/api/buy/' + str(kdb.data['id']), {})
        self.assertEqual(Participant.objects.get(id=caio.data['id']).budget, 100)
        self.assertEqual(Player.objects.get(id=kdb.data['id']).team_participant, None)
        self.assertEqual(result.status_code, 200)

        result = self.client.post('/api/transfers/', {})


        group_1 = self.client.post('/api/group/', {'group': 'Group 1'})
        result = self.client.post('/api/add_participant_group/' + str(group_1.data['id']), {'team': city.data['id']})
        result = self.client.post('/api/add_participant_group/' + str(group_1.data['id']), {'team': united.data['id']})
        result = self.client.post('/api/add_participant_group/' + str(group_1.data['id']), {'team': liverpool.data['id']})
        result = self.client.post('/api/add_participant_group/' + str(group_1.data['id']), {'team': chelsea.data['id']})
        groups = list(Group.objects.all())
        self.assertEqual(len(groups), 1)
        self.assertEqual(len(list(groups[0].teams.all())), 4)
        result = self.client.post('/api/create_matches/' + str(group_1.data['id']))
        matches = result.data

        print("\nMATCHES:")
        for match in matches:
            result = self.client.post('/api/register_score/' + str(match['id']), {'goals_team_1': randint(0,3),
                                                                                  'goals_team_2': randint(0,3)})
            print(Match.objects.get(id=match['id']))

        print('\nGROUP TABLE:')
        table = self.client.get('/api/get_table/' + str(group_1.data['id']))
        table = json.loads(table.data)
        for participant in list(table):
            print(participant)

        self.assertEqual(len(matches), 6)

        result = self.client.post('/api/generate_1st_knockout/')
        semis = result.data

        print("\nSEMIS:")
        for match in semis:
            result = self.client.post('/api/register_score/' + str(match['id']), {'goals_team_1': 2,
                                                                                  'goals_team_2': 0})
            print(Match.objects.get(id=match['id']))

        matches = Match.objects.all()
        self.assertEqual(len(matches), 8)

        result = self.client.post('/api/generate_knockout/' + str(semis[0]['group']))
        final = result.data[0]

        print("\nFINAL:")
        result = self.client.post('/api/register_score/' + str(final['id']), {'goals_team_1': 2,
                                                                              'goals_team_2': 1})
        print(Match.objects.get(id=final['id']))

        matches = Match.objects.all()
        self.assertEqual(len(matches), 9)





