from selenium import webdriver

from bot import instagram_bot
from ig_parser import ig_parser
from ig_filter import ig_filter
from config import config, post_tracker as pt
from scrape_feed import scrape_feed
from unfollow import unfollower
from time import sleep

import json
import geojson
from geojson import FeatureCollection, dump
import arcgis.gis
from arcgis.gis import GIS
from arcgis.features import FeatureLayer




if __name__ == '__main__':

    driver = webdriver.Chrome()
    ig = instagram_bot(driver)
    p = ig_parser(driver)
    f = ig_filter(driver)
    sf = scrape_feed(driver, p, f)
    uf = unfollower(driver)

    ig.login(config.username, config.password)
    
    sf.scrape_feed()

    # continues function until limitations are met
#    while True:
#        if pt.like_counter < config.num_likes:
#            try:
#                sf.scrape_feed()
#                print(f'{pt.like_counter} posts liked.')
#                print(f'{pt.save_counter} posts saved.')
#                sleep(360)
#            except Exception:
#                pass
#        if pt.unfollow_counter < config.num_unfollows:
#            try:
#                uf.unfollow()
#                print(f'{pt.follow_counter} accounts followed.')
#                print(f'{pt.unfollow_counter} accounts unfollowed.')
#            except Exception:
#                pass

    gis = GIS("https://www.arcgis.com", username="sapirdooley_tamu4", password="xyxzeq-7fovBi-jebniq")
    content = arcgis.gis.ContentManager(gis)

    feature_collection = FeatureCollection(pt.saved_posts)

    with open('myfile.geojson', 'w') as f:
        dump(feature_collection, f, indent = 4)

    geojson_path = 'myfile.geojson'
    geojson_properties = {
        'title':'Potential Customers',
        'description':'Based on webscraping data from Instagram',
        'tags':'arcgis, python, TK, GeoJSON,', 
        'type': 'GeoJson',
        'spatialReference': {
            'wkid': 4140
        }
        }
    geojson_item = content.add(geojson_properties, geojson_path)
    geojson_feature = geojson_item.publish()
    
    ig.open_link('https://www.instagram.com/')
    ig.log_out()
    ig.close_browser()

    print(f'{pt.like_counter} posts liked.')
    print(f'{pt.save_counter} posts saved.')
    print(f'{pt.follow_counter} accounts followed.')
    print(f'{pt.unfollow_counter} accounts unfollowed.')
    


        





