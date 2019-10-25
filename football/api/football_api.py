import django
django.setup()

import json
import time
from football.api.api_data import APIData
from football.api.account_info import APIUserData
from football.models import APIMatches, APITables
from datetime import datetime
from football.db.standings import Standings, DBChampionsLeagueGS, DBChampionsLeagueMatches
from football.db.country import Country
from football.db.team import Team
from football.views import search_team_in_db
from datetime import datetime


CODES_LEAGUES = [
    'CL', # Champions_League - Europe
    # 'PL', # Premiere League - England
    # 'ELC', # Championship - England
    #####'FAC', # League One - England
    # 'SA', # Seria A - Italy
    # 'PD', # Primera Division - Spain
    # 'BL1', # Bundesliga - Germany
    # 'FL1', # Ligue 1 - France
    # 'DED', # Eredivisie - Netherlands
    # 'PPL', # Primeira Liga - Portugal
    # 'BSA', # Serie A - Brazil
]


def team_in_db(name):
    return search_team_in_db(name)


def api_matches_data(league_code):

    data = list()

    matches_data = APIData(
        APIUserData.SITE,
        "competitions/{code}/matches".format(code=league_code),
        APIUserData.HEADERS,
    ).data_json()

    matches_data = matches_data.get('matches')

    if matches_data is None:
        return None

    for match in matches_data:

        match_info = dict()

        start_year = match.get('season').get('startDate').split('-')[0]  # TODO регулярное выражение?
        end_year = match.get('season').get('endDate').split('-')[0]
        match_info.update(start_year=start_year, end_year=end_year)

        away_team_name = match.get('awayTeam').get('name')
        match_info.update(away_team=team_in_db(away_team_name)['team_in_db'].id)

        home_team_name = match.get('homeTeam').get('name')
        match_info.update(home_team=team_in_db(home_team_name)['team_in_db'].id)

        group = match.get('group')
        if group and "Group" in group:
            group = group[-1]
        match_info.update(groups=group)

        stage = match.get('stage')
        match_info.update(stage=stage)

        status = match.get('status')
        match_info.update(status=status)

        time_match = match.get('utcDate')
        match_info.update(time_match=time_match)

        score = match.get('score')
        match_info.update(
            away_team_extratime=score.get('extraTime').get('awayTeam'),
            home_team_extratime=score.get('extraTime').get('homeTeam'),
            away_team_fulltime=score.get('fullTime').get('awayTeam'),
            home_team_fulltime=score.get('fullTime').get('homeTeam'),
            away_team_halftime=score.get('halfTime').get('awayTeam'),
            home_team_halftime=score.get('halfTime').get('homeTeam'),
            away_team_penalties=score.get('penalties').get('awayTeam'),
            home_team_penalties=score.get('penalties').get('homeTeam'),
            winner=score.get('winner'),
        )

        last_updated = match.get('lastUpdated')
        match_info.update(last_updated=last_updated)

        data.append(match_info)

        DBChampionsLeagueMatches().insert_team(match_info)
    # return data



def forming_table_name(*args):

    return '_'.join(args)


def api_data_table(league_code):

    data_league = APIData(
        APIUserData.SITE,
        "competitions/{code}/standings".format(code=league_code),
        APIUserData.HEADERS,
    ).data_json()
    info_json = data_league
    if info_json is not None:
        with open('data_table.txt', 'w') as file_leaggue:
            file_leaggue.write(json.dumps(info_json, indent=4, sort_keys=True))
        # print(json.dumps(info_json, indent=4, sort_keys=True))
        # APITables.objects.create(
        #     date=datetime.now(),
        #     tables=info_json,
        #     league_code=league_code,
        # )

# from champions league UEFA - standings

def source_data_conversion_1(league_code='CL'):
    data_league = APIData(
        APIUserData.SITE,
        "competitions/{code}/standings".format(code=league_code),
        APIUserData.HEADERS,
    ).data_json()

    if data_league is not None:
        data = dict()
        start_year = data_league['season']['startDate'].split('-')[0] # TODO регулярное выражение?
        end_year = data_league['season']['endDate'].split('-')[0]
        data.update(start_year=start_year, end_year=end_year )
        for standing in data_league['standings']:
            if standing['type'] == 'TOTAL':
                groups = standing['group'][-1]
                data.update(groups=groups)
                # if not data.get(group, None):
                #     data.update({group: []})
                for team in standing['table']:
                    team_name = team['team']['name']
                    team_in_db = search_team_in_db(team_name)
                    data.update(team_id=team_in_db['team_in_db'].id)
                    # print(team)
                    data.update(team)
                    data.update(lastUPD=datetime.now())
                    #team['team']['name'] = search_team_in_db(team_name).get('team_in_db', None)
                    #data[group].append(team)
                    print(data)
                    print('++'*80)

                    DBChampionsLeagueGS().insert_team(data)



        # api_data_table(data)

if __name__ == "__main__":
    # for code_league in CODES_LEAGUES:
    #     print(code_league)
    api_matches_data('CL')
    # #    source_data_conversion_1(code_league)
    #     print('=='*80)
    #     api_data_table(code_league)
    #     time.sleep(5)

    # source_data_conversion_1('CL')