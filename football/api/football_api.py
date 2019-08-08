import django
django.setup()

import json
import time
from football.api.api_data import APIData
from football.api.account_info import APIUserData
from football.models import APIMatches, APITables
from datetime import datetime
from football.db.standings import Standings, DBChampionsLeagueGS
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

def api_data_league(league_code):
    data_league = APIData(
        APIUserData.SITE,
        "competitions/{code}/matches".format(code=league_code),
        APIUserData.HEADERS,
    )

    info_json = data_league.data_json()
    if info_json is not None:
        with open('data_league.txt', 'w') as file_leaggue:
            file_leaggue.write(json.dumps(info_json, indent=4, sort_keys=True))

        print(json.dumps(info_json, indent=4, sort_keys=True))
        # APIMatches.objects.create(
        #     date=datetime.now(),
        #     data=info_json,
        #     league_code=league_code,
        # )


def forming_table_name(*args):

    return '_'.join(args)


def api_data_table(league_code):

    data_league = APIData(
        APIUserData.SITE,
        "competitions/{code}/standings".format(code=league_code),
        APIUserData.HEADERS,
    )
    info_json = data_league.data_json()
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
        "competitions/{code}/standings?season=2017".format(code=league_code),
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
    #     api_data_league(code_league)
    # #    source_data_conversion_1(code_league)
    #     print('=='*80)
    #     api_data_table(code_league)
    #     time.sleep(5)

    source_data_conversion_1('CL')