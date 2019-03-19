import json
import requests
from football.api.account_info import APIUserData


class APIData:

    def __init__(self, site, request='', headers={}):
        self.site = site
        self.request = request
        self.headers = headers
        self.response = None

    def connect(self):
        self.response = requests.get(self.site + self.request, headers=self.headers)

    def status(self):
        if self.response is None:
            return None

        if self.response.status_code == 200:
            return True
        else:
            return None

    def data(self):
        self.connect()
        if self.status():
            return self.response
        return None

    def data_json(self):
        self.connect()
        if self.status():
            try:
                return self.response.json()
            except json.decoder.JSONDecodeError:
                return None
        return None


if __name__ == "__main__":

    # cl = APIData(APIUserData.SITE, "competitions/CL/matches", APIUserData.HEADERS)
    # print(cl.data_json())
    # val = APIData('http://ip.jsontest.com/ ')
    # print(val.data_json())
    pl_table = APIData(APIUserData.SITE, "competitions/PL/standings", APIUserData.HEADERS)
    print(pl_table.data_json())

