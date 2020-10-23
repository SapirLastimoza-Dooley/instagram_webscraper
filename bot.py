from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException    
from utils import random_sleep
from time import sleep
from dataclasses import dataclass, field
from datetime import datetime
import json

# Holds data from post
@dataclass
class IgPost:
    post_id: str      
    op: str             
    caption: str        
    num_likes: int
    num_hashtags: int
    hashtags: list    
    location: str
    date: datetime


class instagram_bot():

    def __init__(self, driver):
        self.driver = driver

    
    def close_browser(self):
        self.driver.close()

    def login(self, username, password):
        d = self.driver
        d.get('https://instagram.com/')
        sleep(8)
        d.find_element_by_xpath('//input[@name=\'username\']').send_keys(username)
        d.find_element_by_xpath('//input[@name=\'password\']').send_keys(password)
        d.find_element_by_xpath('//div[contains(text(), "Log In")]').click()
        sleep(8)
        d.find_element_by_xpath('//button[contains(text(), "Not Now")]').click()
        random_sleep()
        d.find_element_by_xpath('//button[contains(text(), "Not Now")]').click()
        sleep(8)
 
    def fetch_posts(self, num_posts):
        d = self.driver
        post_links = []
        num_scrolls = round(int(num_posts) / 7)

        for i in range(1, num_scrolls):
            try:
                d.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2)
                links_in_view = d.find_elements_by_tag_name('a')
                links_in_view = [elem.get_attribute('href') for elem in links_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                [post_links.append(link) for link in links_in_view if link not in post_links]
            except Exception:
                continue
        return post_links

    def open_link(self, link):
        self.driver.get(link)

    def like_post(self):
        d = self.driver
        try:
            d.find_element_by_xpath('//*[@aria-label="Like"][@width="24"]').click()
        except NoSuchElementException:
            return False
        return True

    def save_post(self):
        d = self.driver
        try:
            d.find_element_by_xpath('//*[@aria-label="Save"]').click()
        except NoSuchElementException:
            return False
        return True

    def log_out(self):
        d = self.driver
        d.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/span/img').click()
        sleep(2)
        d.find_element_by_xpath('//div[contains(text(), "Log Out")]').click()

    def follow(self):
        d = self.driver
        try:
            d.find_element_by_xpath('//button[contains(text(), "Follow")]').click()
        except NoSuchElementException:
            return False
        return True   
