import django
django.setup()

from football.api.api_data import APIData
from football.api.account_info import APIUserData
from football.models import APIMatches
from datetime import datetime


CODE_LEAGUE = [
    'CL', # Champions_League - Europe
    'PL', # Premiere League - England
]


def champions_league(league_code):
    cl = APIData(
        APIUserData.SITE,
        "competitions/{code}/matches".format(code=league_code),
        APIUserData.HEADERS
    )
    info_json = cl.data_json()
    if info_json is not None:
        APIMatches.objects.create(
            date=datetime.now(),
            data=info_json,
            league_code=league_code
        )


if __name__ == "__main__":
    for code_league in CODE_LEAGUE:
        champions_league(code_league)
