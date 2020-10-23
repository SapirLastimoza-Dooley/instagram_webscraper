from selenium import webdriver

from hashtags import greek_hashtags
from key_words import crossing_keywords

from bot import instagram_bot
from post_parser import ig_post, post_parser
from post_filter import filtered_post, post_filter
from post_tracker import post_tracker
from config import config
from utils import random_sleep

import random
import json


if __name__ == '__main__':

    username = config.username
    password = config.password

    driver = webdriver.Chrome()
    ig = instagram_bot(driver)
    p = post_parser(driver)
    f = post_filter(driver)
    post_tracker = post_tracker()

    ig.login(username, password)
    random_sleep()

    post_links = ig.fetch_posts(config.num_posts)
    random_sleep()

    for i, post_link in enumerate(post_links):
        ig.open_link(post_link)
        post = p.parse_post(post_link)
        filtered_post = f.filter_post(post, config, crossing_keywords)
        random_sleep()

        if filtered_post.does_post_exist == False or \
            filtered_post.is_low_hashtags == False or \
                filtered_post.is_low_likes == False or \
                    filtered_post.is_new_post == False:
            random_sleep()
            continue

        if filtered_post.matches_keyword == True:
            ig.save_post()
            post_tracker.save_counter += 1
            random_sleep()

        like = ig.like_post()
        if like == True:
            post_tracker.like_counter += 1
            random_sleep()

    ig.log_out()


        





