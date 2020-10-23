from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException 

from dataclasses import dataclass
from datetime import datetime
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
    date: datetime
    location: str

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

        
    def parse_post(self, post_link):
        op = self.save_op()
        post_id = post_link
        caption = self.save_caption()
        num_likes = self.find_num_post_likes()
        hashtags = self.save_hashtags()
        num_hashtags = len(hashtags)
        location = self.save_location()
        date = self.find_date()
        
        return ig_post(post_id, op, caption, num_likes, num_hashtags, hashtags, location, date)

