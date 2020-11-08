from selenium import webdriver
from dataclasses import dataclass, field
from datetime import datetime
from dataclass_csv import DataclassReader, dateformat
from config import xpaths


from bot import instagram_bot

# saves information from parsed posts
@dataclass
class ig_post:
    post_link: str
    author: str  
    caption: str      
    num_likes: int      
    hashtags: list      
    num_hashtags: int 
    date: datetime = field(metadata={'dateformat': '%Y-%m-%d'})  
    location: str       
    lat: str            
    lon: str    

@dataclass
class profile:
    profile_link: str
    bio: str
    location: str
    lat: str
    lon: str

class ig_parser(instagram_bot):
    def __init__ (self, driver):
        super().__init__(driver)

    def post_parser(self, post_link: str):
        post_link = post_link
        author = self.save_link(xpaths.author)
        caption = self.save_text(xpaths.caption)
        num_likes = self.save_number(xpaths.likes)
        hashtags = self.save_links(xpaths.hashtags, '.com/explore/')
        num_hashtags = len(hashtags)
        date = self.save_date(xpaths.date)
        location = self.save_text(xpaths.location)
        lat = ''
        lon = ''
        return ig_post(post_link, author, caption, num_likes, hashtags, num_hashtags, date, location, lat, lon)

    def profile_parser(self, profile_link: str, keywords: list):
        profile_link = profile_link
        bio = self.save_text(xpaths.bio)
        location = self.filter_text(bio, keywords)
        lat, lon = self.find_lat_long(location)
        return profile(profile_link, bio, location, lat, lon)
