__author__ = 'Roman Evdokimov'

import time
import os
from parser import site
from bs4 import BeautifulSoup
from selenium import webdriver, common
from parser.data import save_country


WEBDRIVER = "chromedriver"
URL = site.Site.url
allLinks = []

def path_to_driver_browser(webDriver):
    '''Returns path to the webdriver'''
    path = os.path.abspath('../..')
    path += '/drivers/{}'.format(webDriver)

    return path


def run_webdriver(nameDriver):
    path = path_to_driver_browser(nameDriver)

    return webdriver.Chrome(executable_path=path)


def search_list_info(path, page):
    bsobj = BeautifulSoup(page, 'html.parser')
    country_list = bsobj.select(path)
    return country_list


def search_list_teams(driver, num_league, number_row_country):

    list_teams = []

    if num_league % 2 == 1:
        text = "odd"
    elif num_league % 2 == 0:
        text = "even"
    else:
        return None

    if driver.find_element_by_xpath('//li[@class="expandable {}"]'.format(text)):
        driver.find_element_by_xpath(
            '//*[@id = "page_teams_1_block_teams_index_club_teams_2"]'
            '/ul/li[{}]/ul/li[@class="expandable {}"]'.format(number_row_country, text)).click()
        time.sleep(3)
        for team in driver.find_elements_by_xpath(
                '//*[@id = "page_teams_1_block_teams_index_club_teams_2"]'
                '/ul/li[@class = "expandable  expanded loaded"][{}]/ul/li[{}]/ul/li'.format(
                    number_row_country,
                    num_league,
                )):
            list_teams.append(team)
            # print("-" * 8, team.text, "==", team.find_element_by_tag_name("a").get_attribute('href'))
    return list_teams


def open_site(url):
    driver = run_webdriver(WEBDRIVER)
    driver.get(url)
    time.sleep(5)
    page = driver.page_source
    number_row_country = 1
    path_country_list = '#page_teams_1_block_teams_index_club_teams_2 > ul > li'
    for country_info in search_list_info(path_country_list, page):
        ru_name_country = country_info.text.strip()
        save_country(ru_name_country)
        print(country_info.text.strip())
        driver.find_element_by_xpath('//li[@data-area_id="{}"]'.format(country_info["data-area_id"])).click()
        time.sleep(10)
        num_league = 1
        path_leagues = '#page_teams_1_block_teams_index_club_teams_2 > ul >' \
                       'li.expandable.loaded.expanded:nth-child({}) > ul > li'.format(number_row_country)
        for leagues in search_list_info(path_leagues, driver.page_source):
            try:
                # in not leagues
                path_search_leagues = '//*[@id="page_teams_1_block_teams_index_club_teams_2"]' \
                                      '/ul/li[{}]/ul[@class="competitions"]'.format(number_row_country)
                driver.find_element_by_xpath(path_search_leagues)
            except:
                lst_teams = driver.find_element_by_xpath(
                    '//*[@id="page_teams_1_block_teams_index_club_teams_2"]/ul/li[{}]/ul[@class="teams"]'.format(
                        number_row_country))
                for team in lst_teams.find_elements_by_tag_name("a"):
                    print("-" * 8, team.text, '==', team.get_attribute('href'))
                break

            league_name = leagues.text
            print("---- ", league_name)

            teams = search_list_teams(driver, num_league, number_row_country)
            if not teams:
                break

            for team in teams:
                print("-" * 8, team.text, '==', team.find_element_by_tag_name("a").get_attribute('href'))

            num_league += 1

            time.sleep(5)
            if num_league == 4:
                break
        number_row_country += 1
    driver.close()


if __name__ == '__main__':

    open_site(URL)
