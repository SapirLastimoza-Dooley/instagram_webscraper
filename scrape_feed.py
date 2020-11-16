from selenium import webdriver

from bot import instagram_bot
from config import config, post_tracker as pt, xpaths, post_keywords, location_keywords
from utils import random_sleep, convert_to_json
from geojson import Point, Feature
from dataclasses import asdict
import json


class scrape_feed(instagram_bot):
    def __init__ (self, driver, ig_parser, post_filter):
        super().__init__(driver)
        self.ig_parser = ig_parser
        self.post_filter = post_filter

    def scrape_feed(self):
        p = self.ig_parser
        pf = self.post_filter

        # open instagram main page, so that method can be used in loop
        self.open_link('https://www.instagram.com/')
        random_sleep()

        # scroll feed and gather post links from timestamp element
        post_links = self.fetch_posts(config.num_posts)
        random_sleep()

        # loop through post links
        print('Parsing posts...')
        print('-------------------------------------------------------------------------------')
        for i, post_link in enumerate(post_links):
            self.open_link(post_link)
            post = p.post_parser(post_link)
            filtered_post = pf.filter_post(post, config, post_keywords)
            is_relevant_post = pf.is_relevant_post(filtered_post)
            random_sleep()

            # like post
            if config.like_post == True and pt.like_counter < config.num_likes:
                like = self.click_button(xpaths.like_button, 'like button')
                if like == True:
                    pt.like_counter += 1
                else:
                    pt.already_liked_counter += 1

            # breaks if only old posts
#            if pt.already_liked_counter > config.max_already_liked:
#                break
            
            # skips irrelevant posts
            if is_relevant_post == False:
                continue

            # if matched post, save and try to find location
            if filtered_post.matches_keyword == False:
                pt.matched_post_counter += 1
                if config.save_post == True:
                    self.click_button(xpaths.save_button, 'save button')
                    pt.save_counter += 1
                as_json = convert_to_json(post)
                pt.all_posts.append(as_json)
                if post.location != '':
                    try:
                        position = self.find_lat_long(post.location)
                    except ValueError:
                        pass
                    if position != '':
                        self.lat_lon_to_gcs(position, post)
                        point = Point((post.lon, post.lat))
                        date_as_string = post.date.isoformat()
                        short_date = date_as_string[:11]
                        setattr(post, 'date', short_date)
                        pt.posts_with_location.append(Feature(geometry=point, properties = asdict(post)))


#                    try: 
#                        self.open_link(post.author)
#                        profile = p.profile_parser(post.author, location_keywords)
#                        setattr(post, 'lat', profile.lat)
#                        setattr(post, 'lon', profile.lon)
#                    except ValueError:
#                        pass

        print('Making json files.')
        with open("matched_posts.json", "w") as outfile: 
            json.dump(pt.all_posts, outfile, indent = 4)
        with open("matched_posts_locations.json", "w") as outfile: 
            json.dump(pt.posts_with_location, outfile, indent = 4)
        print('-------------------------------------------------------------------------------')

