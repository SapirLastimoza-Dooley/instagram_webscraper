from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException    
from datetime import datetime, timedelta
from dataclasses import dataclass
from config import config
from bot import instagram_bot

@dataclass
class filtered_post:
    matches_keyword: bool
    is_new_post: bool
    is_low_likes: bool
    is_low_hashtags: bool
    does_post_exist: bool

class post_filter(instagram_bot):

    def __init__ (self, driver):
        super().__init__(driver)

    def filter_caption(self, caption, keywords):
        try:
            result = [i for i in keywords if(i in caption)]
        except NoSuchElementException:
            return False            
        return bool(result)

    def filter_date(self, post_date, max_post_age):
        try:
            delta = datetime.now() - post_date
            if delta.days > max_post_age:
                return True
        except NoSuchElementException:
            return False
        
    def filter_likes(self,post_likes, max_likes):
        if post_likes > max_likes:
            return False
        else:
            return True

    def filter_hashtags(self, post_hashtags, max_hashtags):
        if post_hashtags > max_hashtags:
            return False
        else:
            return True

    def find_post_exists(self):
        try:
            self.driver.find_element_by_xpath('//h2[contains(text(), "Sorry"]')
        except NoSuchElementException:
            return True
        return False

    def filter_post(self, post, config, keywords):
        matches_keyword = self.filter_caption(post.caption, keywords)
        is_new_post = self.filter_date(post.date, config.max_post_age)
        is_low_likes = self.filter_likes(post.num_likes, config.max_likes)
        is_low_hashtags =  self.filter_hashtags(post.num_hashtags, config.max_hashtags)
        does_post_exist = self.find_post_exists()
        return filtered_post(matches_keyword, is_new_post, is_low_likes, is_low_hashtags, does_post_exist)