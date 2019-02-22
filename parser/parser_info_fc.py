import requests
import time
import random
from parser.db import FCDataBase
from parser.fc_information_save import save
from bs4 import BeautifulSoup as BS


class ParserInfoFC():

    def __init__(self, url):
        self.url = url
        self.fc_info = {}

    def open_site(self):
        html = requests.get(self.url).text
        return html

    def bs_find_info(self):
        bs_obj = BS(self.open_site(), "html.parser")

        if self.find_not_found_page(bs_obj):
            return False
        self.bs_find_en_name(bs_obj)
        self.bs_find_team_info(bs_obj)
        self.bs_info_stadium(bs_obj)

    def find_not_found_page(self, bs):
        not_found = bs.select_one('#doc4 > h1')
        if not_found:
            if not_found.text == 'Page not found':
                return True
        return False

    def bs_find_en_name(self, bs):
        fc_en_name = bs.select_one("#subheading > h1")
        self.fc_info.update(fc_en_name=fc_en_name.text)

    def bs_find_team_info(self, bs):
        team_info = bs.select_one("#page_team_1_block_team_info_3 > div")

        of_site = team_info.find('p', {'class': 'center website'})
        if not of_site:
            of_site = ''
        else:
            of_site = of_site.a['href']
        self.fc_info.update(official_site=of_site)

        for info in list(zip(team_info.findAll('dt'), team_info.findAll('dd'))):
            key_team = info[0].text.lower()
            value_team = info[1].text.strip()
            self.fc_info.update({key_team: value_team})

        image = team_info.select_one('#page_team_1_block_team_info_3 > div > div.logo > img')
        self.fc_info.update(fc_logo=image['src'])

    def bs_info_stadium(self, bs):
        stadium_info = {}
        stadium_info_on_page = bs.select_one("#page_team_1_block_team_venue_4")

        try:
            for stadium in list(zip(stadium_info_on_page.findAll('dt'), stadium_info_on_page.findAll('dd'))):
                key_team = stadium[0].text.lower()
                value_team = stadium[1].text.strip()
                stadium_info.update({key_team: value_team})
        except AttributeError:
            stadium_info = {'имя': ''}
        try:
            image_stadium = stadium_info_on_page.select_one('#page_team_1_block_team_venue_4 > a > img')
            stadium_info.update(image_stadium=image_stadium['src'])
        except AttributeError:
            stadium_info.update(image_stadium='')

        self.fc_info.update(stadium=stadium_info)



    def get_info_fc(self):
        if self.bs_find_info():
            return False
        return self.fc_info


def parser_data_processing(dct_info):
    address = dct_info.get('адрес', '')
    if address:
        address = ', '.join([loc.strip() for loc in address.split("\n")])

    foundation_year = dct_info.get('основан', 0)
    if foundation_year:
        for val in foundation_year.split('.'):
            if len(val) == 4:
                foundation_year = val
            for val_1 in foundation_year.split(' / '):
                if len(val_1) == 4:
                    foundation_year = val_1
            break

    stadium_info = dct_info.get('stadium', {})
    stadium_info = {
        'stadium_name': stadium_info.get('имя', ''),
        'city': stadium_info.get('город', ''),
        'url_image_stadium': stadium_info.get('image_stadium', ''),
        'capacity': stadium_info.get('вмещает', 0),
    }


    processed_data = {
        'address': address,
        'phone': dct_info.get('телефон', ''),
        'email': dct_info.get('эл. почта', ''),
        'fax': dct_info.get('факс', ''),
        'foundation': foundation_year,
        'official_site': dct_info.get('official_site', ''),
        'fc_en_name': dct_info.get('fc_en_name', ''),
        'fc_logo': dct_info.get('fc_logo'),
        'stadium': stadium_info,
    }

    return processed_data

db = FCDataBase()
#country = country_id(db, "Англия")
id_country = [174, 178]
for country in id_country:
    db.query("""SELECT link_for_parsing, name_id FROM football_parsingdata WHERE country_id = %s OFFSET 3;""",
             (country,))
    num = 1
    for team in db.cursor.fetchall():

        # print(team)
        # if num < 82:
        #     num += 1
        #     continue
        # if num > 85:
        #     break

        parser_info_team = ParserInfoFC(team[0])
        data_fc = parser_info_team.get_info_fc()
        if not data_fc:
            continue
        save(db, parser_data_processing(data_fc), country, team[1])

        print(data_fc['fc_en_name'])

        # if num == 4:
        #     break
        # num += 1
        sec = random.randint(5, 10)
        time.sleep(sec)

db.close()
