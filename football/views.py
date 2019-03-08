from django.shortcuts import render
from .models import FootballClub, ParsingData, CountryRuName, APIChampionsLeague

# Create your views here.

def team_game(name):
    try:
        team = FootballClub.objects.get(fc_en_name=name)
        img = "/fc_logo/{}.png".format(team.num_image)
        return {'team': team, 'image': img}
    except FootballClub.MultipleObjectsReturned:
        team = FootballClub.objects.filter(fc_en_name=name)
        img = "/fc_logo/{}.png".format(team[0].num_image)
        return {'team': team[0], 'image': img}
    except FootballClub.DoesNotExist:
        names = ' '.join([x for x in name.split(' ') if len(x) > 2])
        print('name = ',names)
        try:
            team = FootballClub.objects.get(fc_en_name__contains=names)
            img = "/fc_logo/{}.png".format(team.num_image)
            return {'team': team, 'image': img}
        except FootballClub.MultipleObjectsReturned:
            team = FootballClub.objects.filter(fc_en_name__contains=names)
            img = "/fc_logo/{}.png".format(team[0].num_image)
            return {'team': team[0], 'image': img}
        except FootballClub.DoesNotExist:
            return {'team': name}


def champions_league(request):
    print(FootballClub.objects.filter(fc_en_name='FK Dynamo Kyiv'))


# def champions_league(request):
    datas = APIChampionsLeague.objects.all().order_by('-id')[0]
    data = {'matches': []}

    for match in datas.data['matches']:
        # print(match)
        m = {}
        m.update(stage=match['stage'])
        m.update(homeTeam=team_game(match['homeTeam']['name']))
        m.update(awayTeam=team_game(match['awayTeam']['name']))
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


def league(request, country, league_id):
    teams = []
    # Добавить try/except к ParsingData ?
    for team in ParsingData.objects.filter(country_id=country, league_id=league_id):
        try:
            teams.append(FootballClub.objects.get(fc_id_name_dictionary=team.name_id))
        except FootballClub.DoesNotExist:
            continue
    return render(request, "teams_league.html", {"teams": teams})
