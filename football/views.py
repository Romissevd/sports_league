from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import FootballClub, APIMatches, CodeLeague, APITables, CountryEnName, ChampionsLeagueGroupStage as CLGroup
from datetime import datetime
from football.leagues.champions_leaague import dct_cl_stages


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
                return {'team_in_db': FootballClub.objects.get(id=1546)}
                #return {'team_in_db': name}


def champions_league_start_years():
    return CLGroup.objects.order_by('-start_year').values_list('start_year', flat=True).distinct()


def champions_league(request, stage):

    start_year = request.GET.get('years', datetime.now().year)

    stages = dct_cl_stages[stage]
    standings_group = None
    start_years = champions_league_start_years()

    datas = APIMatches.objects.filter(league_code="CL").order_by('-id')[0]
    data = {'matches': []}

    for match in datas.data['matches']:
        # print(match)
        m = {}
        if match['stage'] in stages:
            m.update(stage=match['stage'])
            m.update(homeTeam=search_team_in_db(match['homeTeam']['name']))
            m.update(awayTeam=search_team_in_db(match['awayTeam']['name']))
            m.update(score={'homeTeam': match['score']['fullTime']['homeTeam'], 'awayTeam': match['score']['fullTime']['awayTeam']})
            data['matches'].append(m)
    # print(data)
    # data = json.loads(data)
    # print(data)

    if stage == 'groups':
        # standings = APITables.objects.filter(league_code="CL").order_by('-id')[0]
        # standings_group = []
        # for result in standings.tables['standings']:
        #     if result['type'] == 'TOTAL':
        #
        #         for club in result['table']:
        #             team = search_team_in_db(club['team']['name'])
        #             club['team']=team
        #         standings_group.append(result)
        #         # print(result)
        #         # print('==='*40)
        # # print(standings)
        # # standings_group = APITables.objects.filter(league_code="CL").order_by('-id')[0]
        standings_group = CLGroup.objects.filter(start_year=start_year).order_by('groups', 'position')

    return render(request, "champions_league.html", {
        "data": data,
        "standings": standings_group,
        "start_years": start_years,
    })


def championship(request, name_country):
    country = CountryEnName.objects.get(country_name=name_country)
    leagues = CodeLeague.objects.filter(country=name_country.capitalize())
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
    standings = table_info.tables["standings"]

    if len(standings) > 0:

        for team in standings[0]['table']: # есть ли 'table' нужно проверить
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

    return render(request, "calendar_games.html", {"data": match_info})
