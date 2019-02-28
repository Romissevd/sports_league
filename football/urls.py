from django.urls import path, re_path
from . import views


urlpatterns = [
    path('champions_league/', views.champions_league, name='cl'),
    path('all_teams/', views.all_teams, name='all_teams'),
    re_path(r'team/(?P<team_name>[\w|\W]+)/', views.team),
]