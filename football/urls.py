from django.urls import path, re_path
from . import views


urlpatterns = [
    path('champions_league/', views.champions_league, name='cl'),
    path('england/', views.championship, {'name_country': 'England'}, name='england'),
    path('spain/', views.championship, {'name_country': 'Spain'}, name='spain'),
    path('italy/', views.championship, {'name_country': 'Italy'}, name='italy'),
    path('germany/', views.championship, {'name_country': 'Germany'}, name='germany'),
    path('ukraine/', views.championship, {'name_country': 'Ukraine'}, name='ukraine'),
    path('france/', views.championship, {'name_country': 'France'}, name='france'),
    path('turkey/', views.championship, {'name_country': 'Turkey'}, name='turkey'),
    path('netherlands/', views.championship, {'name_country': 'Netherlands'}, name='netherlands'),
    path('portugal/', views.championship, {'name_country': 'Portugal'}, name='portugal'),
    re_path(r'team/(?P<team_name>[\w|\W]+)/', views.team),
    re_path(r'(?P<country>[\w|\W]+)/(?P<country_id>[\w|\W]+)/(?P<league_id>[\d]+)/matches', views.matches),
    re_path(r'(?P<country>[\w|\W]+)/(?P<country_id>[\w|\W]+)/(?P<league_id>[\d]+)/calendar', views.calendar_games),
    re_path(r'(?P<country>[\w|\W]+)/(?P<country_id>[\w|\W]+)/(?P<league_id>[\d]+)/table', views.table),
    re_path(r'(?P<country>[\w|\W]+)/(?P<country_id>[\w|\W]+)/(?P<league_id>[\d]+)/', views.league),
]