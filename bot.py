# This is the meat and potatoes of the code, within the class 'instagram_bot()' are all of the functions that interact directly with the webdriver.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException    
from utils import random_sleep
from time import sleep
from datetime import datetime
from config import xpaths
from dataclasses import dataclass
import re

class instagram_bot():

    def __init__(self, driver):
        self.driver = driver

    # closes the browser
    def close_browser(self):
        self.driver.close()

    # opens a link
    def open_link(self, link: str):
        self.driver.get(link)
        random_sleep()

    # logs into the account
    def login(self, username: str, password: str):
        print('Logging in...')
        d = self.driver
        d.get('https://instagram.com/')                                         # opens instagram
        sleep(8)
        d.find_element_by_xpath(xpaths.username_input).send_keys(username)      # finds the username input box and sends the username
        d.find_element_by_xpath(xpaths.password_input).send_keys(password)      # finds the password input box and sends the password
        d.find_element_by_xpath(xpaths.login_button).click()                    # clicks the log-in button
        sleep(8)
        d.find_element_by_xpath(xpaths.popup_button).click()                    # closes the first pop-up
        random_sleep()
        d.find_element_by_xpath(xpaths.popup_button).click()                    # closes the second pop-up
        random_sleep()

    # logs out of the account
    def log_out(self):
        print('Logging out...')
        d = self.driver
        d.find_element_by_xpath(xpaths.dropdown_menu).click()                   # finds the menu button
        sleep(2)
        d.find_element_by_xpath(xpaths.logout_button).click()                   # clicks the log-out button

    # clicks a button
    def click_button(self, xpath: str, button_name):
        d = self.driver
        res = True
        try:
            button = d.find_element_by_xpath(xpath)                             # finds the button by xpath
            button.click()                                                      # clicks the button
            print(f'{button_name} clicked.')
            random_sleep()
        except NoSuchElementException:
            print(f'{button_name} not found.')
            res = False
        print('-------------------------------------------------------------------------------')
        return res

    # scrolls through the instagram feed and saves post links
    def fetch_posts(self, num_posts: int):
        print('Scrolling feed...')
        d = self.driver
        post_links = []                                                                         # holds all post links
        num_scrolls = round(int(num_posts) / 7)                                                 # determines how many scrolls to perform

        for i in range(1, num_scrolls):                                                         # scrolls through feed
            try:
                d.execute_script("window.scrollTo(0, document.body.scrollHeight);")             # scrolls to bottom of page
                sleep(2)
                links_in_view = d.find_elements_by_tag_name('a')                                # gathers all post links in view
                links_in_view = [elem.get_attribute('href') for elem in links_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                [post_links.append(link) for link in links_in_view if link not in post_links]
            except Exception:
                continue
        print('Post fetching complete.')
        return post_links

    # saves all links within view
    def save_links(self, xpath: str, criteria: str):
        d = self.driver
        links = []                                                              # holds all links
        links_in_view = d.find_elements_by_xpath(xpath)                         # finds all links in view
        links_in_view = [elem.get_attribute('href') for elem in links_in_view   # saves all links depending on criteria
                        if criteria in elem.get_attribute('href')]
        [links.append(link) for link in links_in_view if link not in links]
        return links

    # saves one link
    def save_link(self, xpath: str):
        try:
            d = self.driver
            link = d.find_element_by_xpath(xpath)           # finds element by xpath
            link = link.get_attribute('href')               # saves href of element (link)
        except NoSuchElementException:
            return ''
        return link

    def remove_emoji(self, text):
        regrex_pattern = re.compile(pattern = "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            "]+", flags = re.UNICODE)
        return regrex_pattern.sub(r'',text)

    #saves text
    def save_text(self, xpath: str):
        try:
            d = self.driver
            text = d.find_element_by_xpath(xpath).text      # finds element by xpath
            text = text.lower()                             # converts to lowercase
            text = text.replace ('\n', ' ')                 # removes new lines
            no_emoji = self.remove_emoji(text)
            encoded = no_emoji.encode("ascii", "ignore")
            decoded = encoded.decode()
        except NoSuchElementException:
            return ''
        return decoded

    # saves date
    def save_date(self, xpath: str):
        try:
            d = self.driver
            now = datetime.now()                        # if no date is found, todays date is returned
            date = d.find_element_by_xpath(xpath)       # finds date by xpath
            date = date.get_attribute('datetime')       # gets datetime attribute
            date = str(date)                            # converts to string
            date = date[0:10]                           # gets only date and not time
            date = datetime.strptime(date,'%Y-%m-%d')   # sets to YYYY/MM/DD format
        except NoSuchElementException:
            return now
        return date

    # saves a number
    def save_number(self, xpath: str):
        try:
            d = self.driver
            number = d.find_element_by_xpath(xpath).text        # finds element by xpath and converts to text
            number_filter = filter(str.isdigit, number)         # removes all non-digits
            number = ''.join(number_filter)                     
            number = int(number)                                # converts to integer
        except NoSuchElementException:
            return 0
        return number

    # filters text for keyword
    def filter_text(self, text, keywords):
        try:
            result = [i for i in keywords if(i in text)]
        except NoSuchElementException:
            return False            
        return bool(result)


    # opens google and searches for latitude and longitude
    def find_lat_long(self, location):
        print('Attempting to find coordinates...')
        d = self.driver
        d.get('https://www.google.com/')                                                                        # opens google
        random_sleep()
        d.find_element_by_xpath('/html/body/div[2]/div[3]/form/div[2]/div[1]/div[1]/div/div[2]/input').send_keys(location + ' latitude and longitude' + Keys.RETURN)   
        sleep(1)                                   
        try:
            text = d.find_element_by_xpath('//div[@class=\'Z0LcW XcVN5d\']').text                               # lat and lon shows up in two forms -
            res = True
            sleep(1)
        except NoSuchElementException:
            res = False
            try:
                data = d.find_element_by_xpath('//*[@data-attrid="kc:/location/location:coordinates"]')         # - so these account for both forms
                text = data.get_attribute('data-entityname')
                res = True
                sleep(1)
            except NoSuchElementException:
                res = False
        if res == False:
            print('Coordinates could not be found.')
            text = ''
        else:
            print('Coordinates found.')
        print('-------------------------------------------------------------------------------')
        return text

    # converts latitude and longitude to geographic coordinates
    def lat_lon_to_gcs(self, position, post):
        bad_chars = [',','°', ' ', 'N', 'E']     # list characters we dont neet
        lat = position[:10]                                # gets front end of text
        lon = position[11:]                              # gets back end of text
        print(f'Latitude: {lat}')
        print(f'Longitude: {lon}')
        for i in bad_chars:
            lat = lat.replace(i, '')                    # removes bad characters
            lon = lon.replace(i, '')
        if 'S' in lat:                                  # if South, adds negative
            lat = lat.replace('S', '')
            lat = float(lat)
            lat = lat * -1
        else:
            lat = float(lat)
        if 'W' in lon:                                  # if West, adds negative
            lon = lon.replace('W','')
            lon = float(lon)
            lon = lon * -1
        else:
            lon = float(lon)
        print(f'Final Lat: {lat}')
        print(f'Final Lon: {lon}')
        setattr(post, 'lat', lat)
        setattr(post, 'lon', lon)

