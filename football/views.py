from django.shortcuts import render
from .models import FootballClub

# Create your views here.

def all_team(request):
    teams = FootballClub.objects.filter(country__country_name="Англия")
    return render(request, "champions_league.html", {"teams": teams})

def team(request, team_name):
    team_info = FootballClub.objects.get(fc_en_name=team_name)
    img = "/fc_logo/{}.png".format(team_info.num_image)
    return render(request, "team.html", {"team_info": team_info, "image": img})
