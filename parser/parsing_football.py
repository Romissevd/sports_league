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

def open_site(url):
    driver = run_webdriver(WEBDRIVER)
    driver.get(url)
    time.sleep(10)
    page = driver.page_source
    bsObj = BeautifulSoup(page, 'html.parser')

    pos = 1
    for info in bsObj.select('#page_teams_1_block_teams_index_club_teams_2 > ul > li'):

        print(info.text.strip())

        driver.find_element_by_xpath('//li[@data-area_id="{}"]'.format(info["data-area_id"])).click()
        time.sleep(10)
        page_1 = driver.page_source
        bsObj_1 = BeautifulSoup(page_1, 'html.parser')

        num = 1


        for infor in bsObj_1.select('#page_teams_1_block_teams_index_club_teams_2 > ul > li.expandable.loaded.expanded:nth-child({}) > ul > li'.format(pos)):
            try :
                driver.find_element_by_xpath('//*[@id="page_teams_1_block_teams_index_club_teams_2"]/ul/li[{}]/ul[@class="competitions"]'.format(pos))

            except:
                i = driver.find_element_by_xpath(
                    '//*[@id="page_teams_1_block_teams_index_club_teams_2"]/ul/li[{}]/ul[@class="teams"]'.format(
                        pos))
                for inf in i.find_elements_by_tag_name("a"):
                    print("-" * 8, inf.text, '==', inf.get_attribute('href'))
                break

            print("---- ", infor.text)
            if num % 2 == 1 and driver.find_element_by_xpath('//li[@class="expandable odd"]'):
                driver.find_element_by_xpath('//*[@id = "page_teams_1_block_teams_index_club_teams_2"]/ul/li[{}]/ul/li[@class="expandable odd"]'.format(pos)).click()
                time.sleep(3)
                for link in driver.find_elements_by_xpath(
                    '//*[@id = "page_teams_1_block_teams_index_club_teams_2"]/ul/li[@class = "expandable  expanded loaded"][{}]/ul/li[{}]/ul/li'.format(
                        pos, num)):


                    print("-"*8, link.text, "==",link.find_element_by_tag_name("a").get_attribute('href'))

            elif num % 2 == 0 and driver.find_element_by_xpath('//li[@class="expandable even"]'):
                driver.find_element_by_xpath(
                    '//*[@id = "page_teams_1_block_teams_index_club_teams_2"]/ul/li[{}]/ul/li[@class="expandable even"]'.format(
                        pos)).click()

                time.sleep(3)
                for link in driver.find_elements_by_xpath(
                    '//*[@id = "page_teams_1_block_teams_index_club_teams_2"]/ul/li[@class = "expandable  expanded loaded"][{}]/ul/li[{}]/ul/li'.format(
                    pos, num)):
                    print("-"*8, link.text, '==', link.find_element_by_tag_name("a").get_attribute('href'))

            else:
                print("-" * 8, link.text, '==', link.find_element_by_tag_name("a").get_attribute('href'))

            num += 1

            time.sleep(5)
            if num == 4:
                break
        pos += 1
    driver.close()


if __name__ == '__main__':

    open_site(URL)




