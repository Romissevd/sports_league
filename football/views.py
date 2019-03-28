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
        try:
            team = FootballClub.objects.get(alt_name=name)
            img = "/fc_logo/{}.png".format(team.num_image)
            return {'team': team, 'image': img}
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
    datas = APIMatches.objects.filter(league_code="CL").order_by('-id')[0]
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
    try:
        code = CodeLeague.objects.get(country=country.capitalize(), league=league_id)
    except CodeLeague.DoesNotExist:
        return render(request, "matches.html", {})

    league_info = APIMatches.objects.filter(league_code=code.league_code).order_by('-id')[0]
    data = {'matches': []}

    for match in league_info.data['matches']:
        # print(match)
        match_info = {}
        score_home_team = match['score']['fullTime']['homeTeam']
        score_away_team = match['score']['fullTime']['awayTeam']
        if score_home_team is None and score_away_team is None:
            continue
        match_info.update(stage=match['stage'])
        match_info.update(homeTeam=team_game(match['homeTeam']['name']))
        match_info.update(awayTeam=team_game(match['awayTeam']['name']))
        match_info.update(score={'homeTeam': score_home_team, 'awayTeam': score_away_team})
        date = datetime.strptime(match['utcDate'], FORMAT_DATE_JSON)
        match_info.update(date=datetime.strftime(date, FORMAT_DATE))
        data['matches'].append(match_info)

    return render(request, "matches.html", {"data": data})


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

    try:
        code = CodeLeague.objects.get(country=country.capitalize(), league=league_id)
    except CodeLeague.DoesNotExist:
        return render(request, "table.html", {})

    table_info = APITables.objects.filter(league_code=code.league_code).order_by('-id')[0]

    table = []

    # print(table_info)

    for team in table_info.tables["standings"][0]['table']:
        # print(team)
        team_info = team
        team_info.update(team=team_game(team['team']['name']))
        print(team_info)
        print("___"*40)
        table.append(team_info)

    return render(request, "table.html", {"table": table})


def calendar_games(request, country, country_id, league_id):

    try:
        code = CodeLeague.objects.get(country=country.capitalize(), league=league_id)
    except CodeLeague.DoesNotExist:
        return render(request, "matches.html", {})

    league_info = APIMatches.objects.filter(league_code=code.league_code).order_by('-id')[0]
    # data = {'matches': []}
    match_info = {}

    for match in league_info.data['matches']:

        status = match['status']
        if status == "FINISHED":
            continue
        matchday = match['matchday']
        if not match_info.get(matchday):
            match_info.update({matchday: dict()})

        date = datetime.strptime(match['utcDate'], FORMAT_DATE_JSON)
        date_match = datetime.strftime(date, FORMAT_DATE)
        if not match_info[matchday].get(date_match):
            match_info[matchday].update({date_match: dict()})

        time_match = datetime.strftime(date, FORMAT_TIME)
        if not match_info[matchday][date_match].get(time_match):
            match_info[matchday][date_match].update({time_match: list()})

        game = {}
        game.update(homeTeam=team_game(match['homeTeam']['name']))
        game.update(awayTeam=team_game(match['awayTeam']['name']))
        match_info[matchday][date_match][time_match].append(game)

    match_info = OrderedDict(sorted(match_info.items(), key=lambda item: item[0]))

    return render(request, "calendar_games.html", {"data": match_info})
