from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException    
from utils import random_sleep
from time import sleep
from datetime import datetime
from config import xpaths
from dataclasses import dataclass
import re

class instagram_bot():

    def __init__(self, driver):
        self.driver = driver

    def close_browser(self):
        self.driver.close()

    def open_link(self, link: str):
        self.driver.get(link)
        random_sleep()

    def login(self, username: str, password: str):
        d = self.driver
        d.get('https://instagram.com/')
        sleep(8)
        d.find_element_by_xpath(xpaths.username_input).send_keys(username)
        d.find_element_by_xpath(xpaths.password_input).send_keys(password)
        d.find_element_by_xpath(xpaths.login_button).click()
        sleep(8)
        d.find_element_by_xpath(xpaths.popup_button).click()
        random_sleep()
        d.find_element_by_xpath(xpaths.popup_button).click()
        random_sleep()

    def log_out(self):
        d = self.driver
        d.find_element_by_xpath(xpaths.dropdown_menu).click()
        sleep(2)
        d.find_element_by_xpath(xpaths.logout_button).click()

    def click_button(self, xpath: str):
        d = self.driver
        try:
            button = d.find_element_by_xpath(xpath)
            button.click()
            random_sleep()
        except NoSuchElementException:
            return False
        return True

    def fetch_posts(self, num_posts: int):
        d = self.driver
        post_links = []
        num_scrolls = round(int(num_posts) / 7)

        for i in range(1, num_scrolls):
            try:
                d.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2)
                links_in_view = d.find_elements_by_tag_name('a')
                links_in_view = [elem.get_attribute('href') for elem in links_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                [post_links.append(link) for link in links_in_view if link not in post_links]
            except Exception:
                continue
        return post_links

    def save_links(self, xpath: str, criteria: str):
        d = self.driver
        links = []
        links_in_view = d.find_elements_by_xpath(xpath)
        links_in_view = [elem.get_attribute('href') for elem in links_in_view
                        if criteria in elem.get_attribute('href')]
        [links.append(link) for link in links_in_view if link not in links]
        return links

    def save_link(self, xpath: str):
        try:
            d = self.driver
            link = d.find_element_by_xpath(xpath)
            link = link.get_attribute('href')
        except NoSuchElementException:
            return ''
        return link

    def save_text(self, xpath: str):
        try:
            d = self.driver
            text = d.find_element_by_xpath(xpath).text
            text = text.lower()
            text = text.replace ('\n', ' ')
        except NoSuchElementException:
            return ''
        return text

    def save_date(self, xpath: str):
        try:
            d = self.driver
            now = datetime.now()
            date = d.find_element_by_xpath(xpath)
            date = date.get_attribute('datetime')
            date = str(date)
            date = date[0:10]
            date = datetime.strptime(date,'%Y-%m-%d')
        except NoSuchElementException:
            return now
        return date

    def save_number(self, xpath: str):
        try:
            d = self.driver
            number = d.find_element_by_xpath(xpath).text
            number_filter = filter(str.isdigit, number)
            number = ''.join(number_filter)
            number = int(number)
        except NoSuchElementException:
            return 0
        return number

    def filter_text(self, text, keywords):
        try:
            result = [i for i in keywords if(i in text)]
        except NoSuchElementException:
            return []            
        return result

    def find_lat_long(self, location):
        d = self.driver
        d.get('https://www.google.com/')
        d.find_element_by_xpath('/html/body/div[2]/div[3]/form/div[2]/div[1]/div[1]/div/div[2]/input').send_keys(location + ' latitude and longitude' + Keys.RETURN)
        random_sleep()
        try:
            text = d.find_element_by_xpath('//div[@class=\'Z0LcW XcVN5d\']').text
        except NoSuchElementException:
            try:
                data = d.find_element_by_xpath('//*[@data-attrid="kc:/location/location:coordinates"]')
                text = data.get_attribute('data-entityname')
            except NoSuchElementException:
                return ''
        return text

    def lat_lon_to_gcs(self, text):
        bad_chars = [',','\xc2\xb0', ' ', 'N', 'E']
        lat = text[0:10]
        lon = text[-11:-1]
        for i in bad_chars:
            lat = lat.replace(i, '')
            lon = lon.replace(i, '')
        if 'S' in lat:
            lat = lat.replace('S', '')
            lat = float(lat)
            lat = lat * -1
        else:
            lat = float(lat)
        if 'W' in lon:
            lon = lon.replace('w','')
            lon = float(lon)
            lon = lon * -1
        else:
            lon = float(lon)
        return lat, lon

#REMOVE N AND W AND DEGREE


