from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException    
from datetime import datetime, timedelta
from dataclasses import dataclass
from config import config, post_tracker
from bot import instagram_bot
from dataclasses import dataclass
from utils import random_sleep

# saves information on filtered posts
@dataclass
class filtered_post:
    matches_keyword: bool
    is_new_post: bool 
    is_low_likes: bool
    is_low_hashtags: bool
    does_post_exist: bool
    is_user_post: bool

class ig_filter(instagram_bot):

    def __init__ (self, driver):
        super().__init__(driver)

    def filter_date(self, post, post_date, max_post_age):
        try:
            delta = datetime.now() - post_date          # finds time between post is made and now
            if delta.days > max_post_age:
                post_tracker.old_post_counter += 1
                res = False
            else:
                res = True
        except NoSuchElementException:
            pass
        return res
        
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

    def is_user_post(self, post_author, user_profile):
        if post_author == user_profile:
            return True
        else:
            return False

    def filter_post(self, post, config, keywords):
        matches_keyword = self.filter_text(post.caption, keywords)
        is_new_post = self.filter_date(post, post.date, config.max_post_age)
        is_low_likes = self.filter_likes(post.num_likes, config.max_post_likes)
        is_low_hashtags =  self.filter_hashtags(post.num_hashtags, config.max_hashtags)
        does_post_exist = self.find_post_exists()
        is_user_post = self.is_user_post(post.author, config.user_profile)

        print(f'Matches keyword: {matches_keyword}')
        print(f'Is new post: {is_new_post}')
        print(f'Is low likes: {is_low_likes}')
        print(f'Is low hashtags: {is_low_hashtags}')
        print(f'Post exists: {does_post_exist}')
        print(f'Is user post: {is_user_post}')
        print()
        return filtered_post(matches_keyword, is_new_post, is_low_likes, is_low_hashtags, does_post_exist, is_user_post)

    def is_relevant_post(self, filtered_post):
        if filtered_post.does_post_exist == False or \
            filtered_post.is_low_hashtags == False or \
                filtered_post.is_low_likes == False or \
                    filtered_post.is_new_post == False or \
                        filtered_post.is_user_post == True:
            random_sleep()
            res = False
        else:
            res = True
        if res == False:
            print(f'Post is not relevant.')
        else:
            print(f'Post is relevant.')
        print('-------------------------------------------------------------------------------')
        return res
#
#    def is_relevant_post(self, filtered_post):
#        if filtered_post.does_post_exist == False:
#            print('Post does not exist')
#            res = False
#        elif filtered_post.is_low_hashtags == False:
#            res = False
#        elif filtered_post.is_low_likes == False:
#            res = False
#        elif filtered_post.is_new_post == False:
#            res = False
#        elif filtered_post.is_user_post == True:
#            res = False
#        else:
#            res = True
#        
#        if res == False:
#            print('Post is not relevant.')
#        else:
#            print('Post is relevant.')
#        return res



