from django.urls import path, include
from rest_framework import routers
from WebApp.views.Player import PlayerViewSet, BuyPlayerView, TransfersView, ChampzPlayersView, UpdatePlayerDatabaseView
from WebApp.views.Group import GroupViewSet, GetGroupStageView, GetGroupTableView, GetWildcardKnockoutRoundView, GetSemiFinalsRoundView, GetFinalView
from WebApp.views.Participant import ParticipantViewSet, ParticipantsTeamsView
from WebApp.views.Champz import EndChampzView
from WebApp.views.Team import TeamViewSet, UpdateTeamsLeaguesDatabaseView
from WebApp.views.Nation import NationViewSet
from WebApp.views.Match import MatchViewSet
from WebApp.views.Position import PositionViewSet
from WebApp.views.League import LeagueViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('nation', NationViewSet)
router.register('league', LeagueViewSet)
router.register('participant', ParticipantViewSet)
router.register('team', TeamViewSet)
router.register('position', PositionViewSet)
router.register('player', PlayerViewSet)
router.register('group', GroupViewSet)
router.register('match', MatchViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('buy/<int:id>', BuyPlayerView.as_view(), name='post'),
    path('table/<int:id>', GetGroupTableView.as_view(), name='get'),
    path('group-stage', GetGroupStageView.as_view(), name='post'),
    path('wildcards', GetWildcardKnockoutRoundView.as_view(), name='post'),
    path('semis', GetSemiFinalsRoundView.as_view(), name='post'),
    path('final', GetFinalView.as_view(), name='post'),
    path('transfers', TransfersView.as_view(), name='get'),
    path('champz-players', ChampzPlayersView.as_view(), name='get'),
    path('participants-teams', ParticipantsTeamsView.as_view(), name='get'),
    path('end-champz', EndChampzView.as_view(), name='post'),
    path('update-players', UpdatePlayerDatabaseView.as_view(), name='post'),
    path('update-teams-leagues', UpdateTeamsLeaguesDatabaseView.as_view(), name='post'),
]