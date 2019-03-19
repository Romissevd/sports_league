import django
django.setup()

from football.api.api_data import APIData
from football.api.account_info import APIUserData
from football.models import APIMatches, APITables
from datetime import datetime
from football.db.standings import Standings


CODE_LEAGUE = [
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


def api_data_table(league_code):
    data_league = APIData(
        APIUserData.SITE,
        "competitions/{code}/standings".format(code=league_code),
        APIUserData.HEADERS,
    )

    info_json = data_league.data_json()
    if info_json is not None:

        country = info_json['competition']['area']['name']
        start_year = info_json['season']['startDate'].split('-')[0]
        end_year = info_json['season']['endDate'].split('-')[0]

        table_name = '_'.join([country, league_code, start_year, end_year])

        Standings().search_table(table_name)

        # APITables.objects.create(
        #     date=datetime.now(),
        #     tables=info_json,
        #     league_code=league_code,
        # )


if __name__ == "__main__":
    for code_league in CODE_LEAGUE:
        # api_data_league(code_league)
        api_data_table(code_league)
