from selenium import webdriver

from bot import instagram_bot
from config import config, post_tracker as pt, xpaths, post_keywords, location_keywords
from utils import random_sleep, convert_to_json
from ig_parser import spatialReference
from geojson import Point, Feature
from dataclasses import asdict


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
        for i, post_link in enumerate(post_links):
            self.open_link(post_link)
            post = p.post_parser(post_link)
            filtered_post = pf.filter_post(post, config, post_keywords)
            is_relevant_post = pf.is_relevant_post(filtered_post)
            random_sleep()

            # breaks if only old posts
            if pt.already_liked_counter > config.max_already_liked:
                break
            
            # skips irrelevant posts
            if is_relevant_post == False:
                continue

            if bool(filtered_post.matches_keyword) == True:
                pt.matched_post_counter += 1
                self.click_button(xpaths.save_button)
                pt.save_counter += 1

            # if matched post, save and try to find location
            if bool(filtered_post.matches_keyword) == False:
                pt.matched_post_counter += 1
#                self.click_button(xpaths.save_button)
#                pt.save_counter += 1
                if post.location != '':
                    try:
                        position = self.find_lat_long(post.location)
                        if position != '':
                            lat, lon = self.lat_lon_to_gcs(position)
                            setattr(post, 'lat', lat)
                            setattr(post, 'lon', lon)
                            point = Point((post.lon, post.lat))
                            date_as_string = post.date.isoformat()
                            setattr(post, 'date', date_as_string)
                            pt.saved_posts.append(Feature(geometry=point, properties = asdict(post)))
                    except ValueError:
                        pass

#                    try: 
#                        self.open_link(post.author)
#                        profile = p.profile_parser(post.author, location_keywords)
#                        setattr(post, 'lat', profile.lat)
#                        setattr(post, 'lon', profile.lon)
#                    except ValueError:
#                        pass

            # like post
            like = self.click_button(xpaths.like_button)
            if like == True:
                pt.like_counter += 1
            else:
                pt.already_liked_counter += 1