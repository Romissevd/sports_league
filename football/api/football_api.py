import django
django.setup()

import json
from football.api.api_data import APIData
from football.api.account_info import APIUserData
from football.models import APIMatches, APITables
from datetime import datetime
from football.db.standings import Standings
from football.db.country import Country
from football.db.team import Team


CODES_LEAGUES = [
    # 'CL', # Champions_League - Europe
    'PL', # Premiere League - England
    # 'ELC', # Championship - England
    #####'FAC', # League One - England
    'SA', # Seria A - Italy
    'PD', # Primera Division - Spain
    'BL1', # Bundesliga - Germany
    'FL1', # Ligue 1 - France
    'DED', # Eredivisie - Netherlands
    'PPL', # Primeira Liga - Portugal
    'BSA', # Serie A - Brazil
]


def api_data_league(league_code):
    data_league = APIData(
        APIUserData.SITE,
        "competitions/{code}/matches".format(code=league_code),
        APIUserData.HEADERS,
    )

    info_json = data_league.data_json()
    if info_json is not None:
        APIMatches.objects.create(
            date=datetime.now(),
            data=info_json,
            league_code=league_code,
        )


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
        # print(json.dumps(info_json, indent=4, sort_keys=True))
        APITables.objects.create(
            date=datetime.now(),
            tables=info_json,
            league_code=league_code,
        )


# def source_data_conversion_1(league_code):
#     data_league = APIData(
#         APIUserData.SITE,
#         "competitions/{code}/standings".format(code=league_code),
#         APIUserData.HEADERS,
#     ).data_json()
#     data = dict()
#     if data_league is not None:
#         country = data_league['competition']['area']['name']
#         id_ru_name_country = Country().from_en_to_ru(country)
#         start_year = data_league['season']['startDate'].split('-')[0]
#         end_year = data_league['season']['endDate'].split('-')[0]
#         data.update(table_name=forming_table_name(country, league_code, start_year, end_year))
#         for standing in data_league['standings']:
#             if standing['type'] == 'TOTAL':
#                 data.update(teams=[])
#                 for team in standing['table']:
#                     team_name = team['team']['name']
#                     id_team = Team().search_team(team_name, id_ru_name_country)
#                     if id_team is None:
#                         id_team = 1546 # 1546 - None in DB
#                     team.update(id_team=id_team, team_name=team_name)
#                     data['teams'].append(team)
#
#         api_data_table(data)

if __name__ == "__main__":
    for code_league in CODES_LEAGUES:
        api_data_league(code_league)
        # source_data_conversion_1(code_league)
        api_data_table(code_league)
