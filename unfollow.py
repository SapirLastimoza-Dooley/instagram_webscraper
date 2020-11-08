from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException    
from selenium.webdriver.common.action_chains import ActionChains



from bot import instagram_bot
from config import config, xpaths, post_tracker as pt
from time import sleep
from utils import random_sleep


import utils

class unfollower(instagram_bot):
    def __init__ (self, driver):
        super().__init__(driver)


    def get_profiles(self, button_xpath: str, count_xpath: str):
        d = self.driver
        profile_list = []
        actions = ActionChains(d) 
        press_tab = actions.send_keys(Keys.TAB)

        self.open_link(config.user_profile)         # open user proile
        self.click_button(button_xpath)             # click follow(er/ing) button
        num = int(self.save_number(count_xpath))    # save number follow(er/ing)
        press_tab.perform()                         # skips 'x' button

        # scroll through dialog, collecting profile links
        while len(profile_list) < num - 10:
            try:
                profiles_in_view = self.save_links(xpaths.profile_link, '.com/')
                [profile_list.append(x) for x in profiles_in_view if x not in profile_list] 
                for _ in range(len(profiles_in_view) * 3):
                    press_tab.perform()
                sleep(0.5)
            except NoSuchElementException:
                continue
            print(len(profile_list))
        random_sleep()       
        return profile_list

    def unfollow(self):
        blacklist = []

        # compare lists to see who you follow but does not follow back
        followers = set(self.get_profiles(xpaths.followers_button, xpaths.followers_count))
        following = set(self.get_profiles(xpaths.following_button, xpaths.following_count))
        targetusers = following - followers

        for acc in targetusers:
            blacklist.append(acc)

        # write list to file
        with open('blacklist.txt', 'w') as f:
            for item in blacklist:
                f.write("%s\n" % item)
        print('blacklist created')

        # loop through list and unfollow
        for acc in blacklist:
            self.open_link(acc)
            random_sleep()
            self.click_button(xpaths.friend_follow_button)
            random_sleep()
            self.click_button(xpaths.unfollow_button)
            random_sleep()
            self.click_button(xpaths.follow_back_button)

            pt.unfollow_counter += 1

    def re_follow(self):
        blacklist = open('blacklist.txt', 'r')
        
        # loop through list and re-follow
        for acc in blacklist:
            self.open_link(acc)
            random_sleep()
            self.click_button(xpaths.friend_follow_button)
            random_sleep()
            self.click_button(xpaths.follow_button)
            random_sleep()

            pt.follow_counter += 1


        


    