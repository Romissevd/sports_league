import django
django.setup()

from football.api.api_data import APIData
from football.api.account_info import APIUserData
from football.models import APIChampionsLeague
from datetime import datetime


def champions_league():
    cl = APIData(APIUserData.SITE, "competitions/CL/matches", APIUserData.HEADERS)
    info_json = cl.data_json()
    if info_json is not None:
        APIChampionsLeague.objects.create(date=datetime.now(), data=info_json)


if __name__ == "__main__":
    champions_league()
