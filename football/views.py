from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import FootballClub, ParsingData, CountryRuName, APIMatches, CodeLeague, APITables
from datetime import datetime
from collections import OrderedDict
from football.db.standings import Standings


FORMAT_DATE = "%d-%B-%Y"
FORMAT_TIME = "%H:%M"
FORMAT_DATE_JSON = "%Y-%m-%dT%H:%M:%SZ"
SEASON = 2018

# Create your views here.


def search_team_in_db(name):
    try:
        team = FootballClub.objects.get(fc_en_name=name)
        img = "/fc_logo/{}.png".format(team.num_image)
        return {'team_in_db': team, 'image': img}
    except FootballClub.MultipleObjectsReturned:
        team = FootballClub.objects.filter(fc_en_name=name)
        club = team[0]
        for t in team:
            if club.num_image > t.num_image:
                club = t
        img = "/fc_logo/{}.png".format(club.num_image)
        return {'team_in_db': club, 'image': img}
    except FootballClub.DoesNotExist:
        try:
            team = FootballClub.objects.get(alt_name=name)
            img = "/fc_logo/{}.png".format(team.num_image)
            return {'team_in_db': team, 'image': img}
        except FootballClub.DoesNotExist:
            names = ' '.join([x for x in name.split(' ') if len(x) > 2])
            try:
                team = FootballClub.objects.get(fc_en_name__contains=names)
                img = "/fc_logo/{}.png".format(team.num_image)
                return {'team_in_db': team, 'image': img}
            except FootballClub.MultipleObjectsReturned:
                team = FootballClub.objects.filter(fc_en_name__contains=names)
                club = team[0]
                for t in team:
                    if club.num_image > t.num_image:
                        club = t
                img = "/fc_logo/{}.png".format(club.num_image)
                return {'team_in_db': club, 'image': img}
            except FootballClub.DoesNotExist:
                return {'team_in_db': name}


def champions_league(request):
    # print(FootballClub.objects.filter(fc_en_name='FK Dynamo Kyiv'))
    datas = APIMatches.objects.filter(league_code="CL").order_by('-id')[0]
    data = {'matches': []}

    for match in datas.data['matches']:
        # print(match)
        m = {}
        m.update(stage=match['stage'])
        m.update(homeTeam=search_team_in_db(match['homeTeam']['name']))
        m.update(awayTeam=search_team_in_db(match['awayTeam']['name']))
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

    return HttpResponseRedirect('table')


def matches(request, country, country_id, league_id):
    try:
        code = CodeLeague.objects.get(country=country.capitalize(), league=league_id)
    except CodeLeague.DoesNotExist:
        return render(request, "matches.html", {})
    try:
        league_info = APIMatches.objects.filter(league_code=code.league_code).order_by('-id')[0]
    except IndexError:
        return render(request, "matches.html", {})

    data = {'matches': []}

    for match in league_info.data['matches']:
        match_info = {}
        score_home_team = match['score']['fullTime']['homeTeam']
        score_away_team = match['score']['fullTime']['awayTeam']
        if score_home_team is None and score_away_team is None:
            continue
        match_info.update(stage=match['stage'])
        match_info.update(homeTeam=search_team_in_db(match['homeTeam']['name']))
        match_info.update(awayTeam=search_team_in_db(match['awayTeam']['name']))
        match_info.update(score={'homeTeam': score_home_team, 'awayTeam': score_away_team})
        date = datetime.strptime(match['utcDate'], FORMAT_DATE_JSON)
        match_info.update(date=datetime.strftime(date, FORMAT_DATE))
        data['matches'].append(match_info)

    return render(request, "matches.html", {"data": data})


def table(request, country, country_id, league_id):

    try:
        code = CodeLeague.objects.get(country=country.capitalize(), league=league_id)
    except CodeLeague.DoesNotExist:
        return render(request, "table.html", {})

    try:
        table_info = APITables.objects.filter(league_code=code.league_code).order_by('-id')[0]
        # TODO берется последнее значение в БД по id, может лучше по дате? И проверить
        #  результат должен удовлетворять нашему запросу
    except IndexError:
        return render(request, "table.html", {})

    table = []

    for team in table_info.tables["standings"][0]['table']:
        team_info = team
        team_info.update(team=search_team_in_db(team['team']['name']))
        table.append(team_info)

    return render(request, "table.html", {"table": table})


def calendar_games(request, country, country_id, league_id):

    try:
        code = CodeLeague.objects.get(country=country.capitalize(), league=league_id)
    except CodeLeague.DoesNotExist:
        return render(request, "matches.html", {})

    match_info = []

    try:
        league_info = APIMatches.objects.filter(league_code=code.league_code).order_by('-id')[0]
        # TODO берется последнее значение в БД по id, может лучше по дате? И проверить
        #  результат должен удовлетворять нашему запросу
    except IndexError:
        return render(request, "calendar_games.html", {"data": match_info})


    for match in league_info.data['matches']:
        match_dt = dict()
        status = match['status']
        if status == "FINISHED":
            continue

        match_dt.update(matchday=match['matchday'])

        date = datetime.strptime(match['utcDate'], FORMAT_DATE_JSON)
        date_match = datetime.strftime(date, FORMAT_DATE)
        match_dt.update(date_match=date_match)

        time_match = datetime.strftime(date, FORMAT_TIME)
        match_dt.update(time_match=time_match)

        game = {}
        game.update(homeTeam=search_team_in_db(match['homeTeam']['name']))
        game.update(awayTeam=search_team_in_db(match['awayTeam']['name']))
        match_dt.update(game=game)
        match_info.append(match_dt)

    # match_info = OrderedDict(sorted(match_info.items(), key=lambda item: item[0] and sorted(item[1].items(), key=lambda i: i[0])))
    return render(request, "calendar_games.html", {"data": match_info})
