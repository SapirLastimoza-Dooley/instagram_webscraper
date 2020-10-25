from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException 
from dataclasses import dataclass, field
from datetime import datetime
from dataclass_csv import DataclassReader, dateformat
from utils import random_sleep


import config

from bot import instagram_bot

@dataclass
class ig_post:
    post_id: str
    op: str
    caption: str
    num_likes: int
    num_hashtags: int
    hashtags: list    
    location: str
    date: datetime = field(metadata={'dateformat': '%Y-%m-%d'})
    location: str
    lat: str
    lon: str

class post_parser(instagram_bot):

    def __init__ (self, driver):
        super().__init__(driver)

    def save_caption(self):
        try:
            caption = self.driver.find_element_by_class_name('C4VMK').text
            caption = caption.lower()
            caption = caption.replace('\n', ' ')
        except NoSuchElementException:
            return ''
        return caption

    def save_hashtags(self):
        try:
            hashtags = self.driver.find_elements_by_class_name('xil3i')
            hashtags = [elem.get_attribute('href') for elem in hashtags
                                 if '.com/explore/' in elem.get_attribute('href')]
        except NoSuchElementException:
            return []
        return hashtags

    def save_op(self):
        try:
            op = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/span/a')
            op = op.get_attribute('href')
        except NoSuchElementException:
            return ''
        return op

    def find_num_post_likes(self):
        try: 
            temp = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div[2]/button/span').text
            likes = temp.replace(',', '')
            num_likes = int(likes)
        except NoSuchElementException:
            return 0
        return num_likes       

    def save_location(self):
        try:
            location = self.driver.find_element_by_class_name('O4GlU').text
        except NoSuchElementException:
            return '' 
        return location

    def find_date(self):
        time_now = datetime.now()
        try: 
            temp = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/div[2]/a/time')
            date = temp.get_attribute('datetime')
            date_as_string = str(date)
            simplified = date_as_string[0:10]
            post_date = datetime.strptime(simplified,'%Y-%m-%d')
        except NoSuchElementException:
            return time_now        
        return post_date

    def find_lat_long(self, post):
        d = self.driver
        location = post.location
        d.get('https://www.google.com/')
        d.find_element_by_xpath('/html/body/div[2]/div[3]/form/div[2]/div[1]/div[1]/div/div[2]/input').send_keys(location + ' latitude and longitude' + Keys.RETURN)
        random_sleep()
        lat = ''
        lon = ''
        try:
            text = d.find_element_by_xpath('//div[@class=\'Z0LcW XcVN5d\']').text
            lat = text[0:7]
            lon = text[12:19]
        except NoSuchElementException:
            try:
                data = d.find_element_by_xpath('//*[@data-attrid="kc:/location/location:coordinates"]')
                text = data.get_attribute('data-entityname')
                lat = text[0:7]
                lon = text[12:19]
            except NoSuchElementException:
                return lat, lon
        return lat, lon
        
    def parse_post(self, post_link):
        op = self.save_op()
        post_id = post_link
        caption = self.save_caption()
        num_likes = self.find_num_post_likes()
        hashtags = self.save_hashtags()
        num_hashtags = len(hashtags)
        location = self.save_location()
        date = self.find_date()
        lat = ''
        lon = ''
        
        return ig_post(post_id, op, caption, num_likes, num_hashtags, hashtags, location, date, lat, lon)

