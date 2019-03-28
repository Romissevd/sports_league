import django
django.setup()

from football.api.api_data import APIData
from football.api.account_info import APIUserData
from football.models import APIMatches, APITables
from datetime import datetime
from football.db.standings import Standings
from football.db.country import Country
from football.db.team import Team


CODES_LEAGUES = [
    # 'CL', # Champions_League - Europe
    # 'PL', # Premiere League - England
    'SA', # Seria A - Italy
    'PD', # Primera Division - Spain
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


def api_data_table(data):

    Standings().create_table(data['table_name'])


        # APITables.objects.create(
        #     date=datetime.now(),
        #     tables=info_json,
        #     league_code=league_code,
        # )


def source_data_conversion_1(league_code):
    data_league = APIData(
        APIUserData.SITE,
        "competitions/{code}/standings".format(code=league_code),
        APIUserData.HEADERS,
    ).data_json()
    data = dict()
    if data_league is not None:
        country = data_league['competition']['area']['name']
        id_ru_name_country = Country().from_en_to_ru(country)
        start_year = data_league['season']['startDate'].split('-')[0]
        end_year = data_league['season']['endDate'].split('-')[0]
        data.update(table_name=forming_table_name(country, league_code, start_year, end_year))
        for standing in data_league['standings']:
            data.update(teams=[])
            if standing['type'] == 'TOTAL':
                for team in standing['table']:
                    team_name = team['team']['name']
                    id_team = Team().search_team(team_name, id_ru_name_country)
                    # add_team = team
                    # id_team = get_id_team()
                    # print(team)
                    print(id_team)
                    print("--" * 40)

if __name__ == "__main__":
    for code_league in CODES_LEAGUES:
        # api_data_league(code_league)
        source_data_conversion_1(code_league)
        # api_data_table(code_league)
