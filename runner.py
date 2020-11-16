from selenium import webdriver

from bot import instagram_bot
from ig_parser import ig_parser
from ig_filter import ig_filter
from config import config, post_tracker as pt
from scrape_feed import scrape_feed
from unfollow import unfollower
from time import sleep
from save_to_map import save_to_arcgis_online, create_map
import json
import geojson

if __name__ == '__main__':

    driver = webdriver.Chrome()
    ig = instagram_bot(driver)
    p = ig_parser(driver)
    f = ig_filter(driver)
    sf = scrape_feed(driver, p, f)
    uf = unfollower(driver)

    ig.login(config.insta_username, config.insta_password)
    
    sf.scrape_feed()

    # unfollow those who do not follow
#    uf.unfollow()

    # save to arcGIS Online
    save_to_arcgis_online(config.arcgis_username, config.arcgis_password)
   # create_map()
    
    ig.open_link('https://www.instagram.com/')
    ig.log_out()
    ig.close_browser()
    
    print(f'{len(pt.all_posts)} posts with matching keyword found.')
    print(f'{len(pt.posts_with_location)} posts with keyword and location found.')
    print(f'{pt.like_counter} posts liked.')
    print(f'{pt.save_counter} posts saved.')
    print(f'{pt.follow_counter} accounts followed.')
    print(f'{pt.unfollow_counter} accounts unfollowed.')
    


        





