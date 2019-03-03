from django.shortcuts import render
from .models import FootballClub, ParsingData, CountryRuName

# Create your views here.


def champions_league(request):
    teams = FootballClub.objects.filter(country__country_name="Англия")
    return render(request, "champions_league.html", {"teams": teams})


def championship(request, ru_name_country):
    country = CountryRuName.objects.get(country_name=ru_name_country)
    leagues = ParsingData.objects.filter(country_id=country.id).distinct('league_id')
    return render(request, "country_leagues.html", {"leagues": leagues, "country": country})


def team(request, team_name):
    team_info = FootballClub.objects.get(fc_en_name=team_name)
    img = "/fc_logo/{}.png".format(team_info.num_image)
    return render(request, "team.html", {"team_info": team_info, "image": img})


def league(request, country, league_id):
    teams = []
    for team in ParsingData.objects.filter(country_id=country, league_id=league_id):
        try:
            teams.append(FootballClub.objects.get(fc_id_name_dictionary=team.name_id))
        except FootballClub.DoesNotExist:
            continue
    return render(request, "teams_league.html", {"teams": teams})
