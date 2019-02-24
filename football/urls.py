from django.urls import path, re_path
from . import views


urlpatterns = [
    path('champions_league/', views.all_team, name='all_team'),
    re_path(r'team/(?P<team_name>[\w|\W]+)/', views.team),
]