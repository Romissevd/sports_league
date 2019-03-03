from django.shortcuts import render
from .models import FootballClub, ParsingData, CountryRuName

# Create your views here.


def champions_league(request):
    teams = FootballClub.objects.filter(country__country_name="Англия")
    return render(request, "champions_league.html", {"teams": teams})


def championship(request, ru_name_country):
    country = CountryRuName.objects.get(country_name=ru_name_country)
    teams = FootballClub.objects.filter(country__country_name=ru_name_country)
    leag = []
    print(len(teams))
    for team in teams:
        info = ParsingData.objects.get(name_id=team.fc_id_name_dictionary, country_id=country.id)
        leag.append({
            'league': info.league_id.league_name,
            'team_name': info.name_id.club_name,
            'fc_en_name': team.fc_en_name,
        }
        )
    leag = sorted(leag, key=lambda k: k['league'])
    return render(request, "champions_league.html", {"leagues": leag})


def team(request, team_name):
    team_info = FootballClub.objects.get(fc_en_name=team_name)
    img = "/fc_logo/{}.png".format(team_info.num_image)
    return render(request, "team.html", {"team_info": team_info, "image": img})


def all_teams(request):
    teams = FootballClub.objects.all()
    data = ParsingData.objects.all()

    return render(request, "all_teams.html", {"teams": teams, "data": data})
