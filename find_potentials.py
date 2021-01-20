from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException    
from selenium.webdriver.common.action_chains import ActionChains



from bot import instagram_bot
from config import config, xpaths, post_tracker as pt
from time import sleep
from utils import random_sleep
from bot import instagram_bot
from config import config, post_tracker as pt, xpaths, post_keywords, location_keywords
from utils import random_sleep, convert_to_json
from geojson import Point, Feature
from dataclasses import asdict
import json

class find_potentials(instagram_bot):
    def __init__ (self, driver, ig_parser, post_filter):
        super().__init__(driver)
        self.ig_parser = ig_parser
        self.post_filter = post_filter

    def collect_accounts(self, button_xpath, count_xpath):
        matched_accounts = []
        all_accounts = []
        d = self.driver
        p = self.ig_parser
        pf = self.post_filter
        actions = ActionChains(d) 
        press_tab = actions.send_keys(Keys.TAB)

        self.open_link('https://www.instagram.com/tamuvsa/?hl=en')
        random_sleep()

        accounts = self.click_button(xpaths.followers_button, "followers")
        num = int(self.save_number(count_xpath))    # save number follow(er/ing)
        press_tab.perform()    

        while len(accounts) < num - 10:
            try:
                profiles_in_view = self.save_links(xpaths.profile_link, '.com/')
                [all_accounts.append(x) for x in profiles_in_view if x not in all_accounts] 
                for _ in range(len(profiles_in_view) * 3):
                    press_tab.perform()
                sleep(0.5)
            except NoSuchElementException:
                continue
            print(len(all_accounts))
        random_sleep()       

        for acc in enumerate(all_accounts):
            self.open_link(acc)
            profile = p.profile_parser(acc)
            filtered_profile = pf.filter_profile(acc, config, post_keywords)


            if filtered_profile.matches_keyword == True:
                matched_accounts.append(acc.bio)

        with open("matched_profiles.json", "w") as outfile: 
            json.dump(matched_accounts, outfile, indent = 4)
