from django.urls import path, re_path
from . import views


urlpatterns = [
    path('champions_league/', views.champions_league, name='cl'),
    path('england/', views.championship, {'ru_name_country': 'Англия'}, name='england'),
    path('spain/', views.championship, {'ru_name_country': 'Испания'}, name='spain'),
    path('italy/', views.championship, {'ru_name_country': 'Италия'}, name='italy'),
    path('germany/', views.championship, {'ru_name_country': 'Германия'}, name='germany'),
    path('ukraine/', views.championship, {'ru_name_country': 'Украина'}, name='ukraine'),
    path('france/', views.championship, {'ru_name_country': 'Франция'}, name='france'),
    path('turkey/', views.championship, {'ru_name_country': 'Турция'}, name='turkey'),
    path('all_teams/', views.all_teams, name='all_teams'),
    re_path(r'team/(?P<team_name>[\w|\W]+)/', views.team),
]