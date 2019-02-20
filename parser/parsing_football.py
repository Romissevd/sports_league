__author__ = 'Roman Evdokimov'

import time
import os
from parser import site
from bs4 import BeautifulSoup
from selenium import webdriver, common


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
    bsObj = BeautifulSoup(page, 'html.parser')
    country_list = bsObj.select(path)
    return country_list



def open_site(url):
    driver = run_webdriver(WEBDRIVER)
    driver.get(url)
    time.sleep(5)
    page = driver.page_source
    number_row = 1
    path_country_list = '#page_teams_1_block_teams_index_club_teams_2 > ul > li'
    for country_info in search_list_info(path_country_list, page):
        rus_name_country = country_info.text.strip()
        print(country_info.text.strip())
        driver.find_element_by_xpath('//li[@data-area_id="{}"]'.format(country_info["data-area_id"])).click()
        time.sleep(10)
        num = 1
        path_leagues = '#page_teams_1_block_teams_index_club_teams_2 > ul > li.expandable.loaded.expanded:nth-child({}) > ul > li'.format(number_row)
        for leagues in search_list_info(path_leagues, driver.page_source):
            try:
                # in not leagues
                path_search_leagues = '//*[@id="page_teams_1_block_teams_index_club_teams_2"]/ul/li[{}]/ul[@class="competitions"]'.format(number_row)
                driver.find_element_by_xpath(path_search_leagues)
            except:
                lst_clubs = driver.find_element_by_xpath(
                    '//*[@id="page_teams_1_block_teams_index_club_teams_2"]/ul/li[{}]/ul[@class="teams"]'.format(
                        number_row))
                for club in lst_clubs.find_elements_by_tag_name("a"):
                    print("-" * 8, club.text, '==', club.get_attribute('href'))
                break

            league_name = leagues.text

            print("---- ", league_name)
            if num % 2 == 1 and driver.find_element_by_xpath('//li[@class="expandable odd"]'):
                driver.find_element_by_xpath('//*[@id = "page_teams_1_block_teams_index_club_teams_2"]/ul/li[{}]/ul/li[@class="expandable odd"]'.format(number_row)).click()
                time.sleep(3)
                for link in driver.find_elements_by_xpath(
                    '//*[@id = "page_teams_1_block_teams_index_club_teams_2"]/ul/li[@class = "expandable  expanded loaded"][{}]/ul/li[{}]/ul/li'.format(
                        number_row, num)):


                    print("-"*8, link.text, "==",link.find_element_by_tag_name("a").get_attribute('href'))

            elif num % 2 == 0 and driver.find_element_by_xpath('//li[@class="expandable even"]'):
                driver.find_element_by_xpath(
                    '//*[@id = "page_teams_1_block_teams_index_club_teams_2"]/ul/li[{}]/ul/li[@class="expandable even"]'.format(
                        number_row)).click()

                time.sleep(3)
                for link in driver.find_elements_by_xpath(
                    '//*[@id = "page_teams_1_block_teams_index_club_teams_2"]/ul/li[@class = "expandable  expanded loaded"][{}]/ul/li[{}]/ul/li'.format(
                    number_row, num)):
                    print("-"*8, link.text, '==', link.find_element_by_tag_name("a").get_attribute('href'))

            else:
                break

            num += 1

            time.sleep(5)
            if num == 4:
                break
        number_row += 1
    driver.close()


if __name__ == '__main__':

    open_site(URL)




