import requests
from parser.db import FCDataBase
from parser.data import country_id
from bs4 import BeautifulSoup as BS


class ParserInfoFC():

    def __init__(self, url):
        self.url = url
        self.fc_info = {}

    def open_site(self, url):
        html = requests.get(url).text
        return html

    def bs_find_info(self):
        bs_obj = BS(self.open_site(self.url), "html.parser")
        self.bs_find_en_name(bs_obj)
        self.bs_find_team_info(bs_obj)

    def bs_find_en_name(self, bs):
        en_name = bs.select_one("#subheading > h1")
        self.fc_info.update(en_name=en_name.text)

    def bs_find_team_info(self, bs):
        team_info = bs.select_one("#page_team_1_block_team_info_3 > div")

        of_site = team_info.find('p', {'class': 'center website'})
        if not of_site:
            of_site = ''
        self.fc_info.update(official_site=of_site.a['href'])

        for info in list(zip(team_info.findAll('dt'), team_info.findAll('dd'))):
            key_team = info[0].text.lower()
            value_team = info[1].text.strip().lower()
            self.fc_info.update({key_team: value_team})

        image = team_info.select_one('#page_team_1_block_team_info_3 > div > div.logo > img')
        self.fc_info.update(image=image['src'])


    def get_info_fc(self):
        self.bs_find_info()
        return self.fc_info


db = FCDataBase()
country = country_id(db, "Англия")
db.query("""SELECT link_for_parsing FROM football_parsingdata WHERE country_id = %s;""",
         (country,))
num = 1
for url_team in db.cursor:

    parser_info_team = ParserInfoFC(url_team[0])
    print(parser_info_team.get_info_fc())
    # print(requests.get(url_team[0]).text)
    if num == 1:
        break
    num += 1

db.close()
