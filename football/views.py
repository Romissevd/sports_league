from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import FootballClub, ParsingData, CountryRuName, APIMatches

# Create your views here.

def team_game(name):
    try:
        team = FootballClub.objects.get(fc_en_name=name)
        img = "/fc_logo/{}.png".format(team.num_image)
        return {'team': team, 'image': img}
    except FootballClub.MultipleObjectsReturned:
        team = FootballClub.objects.filter(fc_en_name=name)
        club = team[0]
        for t in team:
            if club.num_image > t.num_image:
                club = t
        img = "/fc_logo/{}.png".format(club.num_image)
        return {'team': club, 'image': img}
    except FootballClub.DoesNotExist:
        names = ' '.join([x for x in name.split(' ') if len(x) > 2])
        try:
            team = FootballClub.objects.get(fc_en_name__contains=names)
            img = "/fc_logo/{}.png".format(team.num_image)
            return {'team': team, 'image': img}
        except FootballClub.MultipleObjectsReturned:
            team = FootballClub.objects.filter(fc_en_name__contains=names)
            club = team[0]
            for t in team:
                if club.num_image > t.num_image:
                    club = t
            img = "/fc_logo/{}.png".format(club.num_image)
            return {'team': club, 'image': img}
        except FootballClub.DoesNotExist:
            return {'team': name}


def champions_league(request):
    # print(FootballClub.objects.filter(fc_en_name='FK Dynamo Kyiv'))
    datas = APIMatches.objects.all().order_by('-id')[0]
    data = {'matches': []}

    for match in datas.data['matches']:
        # print(match)
        m = {}
        m.update(stage=match['stage'])
        m.update(homeTeam=team_game(match['homeTeam']['name']))
        m.update(awayTeam=team_game(match['awayTeam']['name']))
        m.update(score={'homeTeam': match['score']['fullTime']['homeTeam'], 'awayTeam': match['score']['fullTime']['awayTeam']})
        data['matches'].append(m)
    # print(data)
    # data = json.loads(data)
    # print(data)
    return render(request, "champions_league.html", {"data": {"data": data}})


def championship(request, ru_name_country):
    country = CountryRuName.objects.get(country_name=ru_name_country)
    leagues = ParsingData.objects.filter(country_id=country.id).distinct('league_id')
    return render(request, "country_leagues.html", {"leagues": leagues, "country": country})


def team(request, team_name):
    team_info = FootballClub.objects.get(fc_en_name=team_name)
    img = "/fc_logo/{}.png".format(team_info.num_image)
    return render(request, "team.html", {"team_info": team_info, "image": img})


def league(request, country, country_id, league_id):

    return HttpResponseRedirect('teams')


def matches(request, country, country_id, league_id):

    return render(request, "matches.html")


def teams(request, country,  country_id, league_id):
    teams = []
    # Добавить try/except к ParsingData ?
    for team in ParsingData.objects.filter(country_id=country_id, league_id=league_id):
        try:
            teams.append(FootballClub.objects.get(fc_id_name_dictionary=team.name_id, country_id=country_id))
        except FootballClub.DoesNotExist:
            continue

    return render(request, "teams.html",  {"teams": teams})


def table(request, country, country_id, league_id):

    return render(request, "table.html")


def calendar_games(request, country, country_id, league_id):

    return render(request, "calendar_games.html")