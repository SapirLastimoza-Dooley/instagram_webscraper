from selenium import webdriver
from time import sleep
from credentials import pw
from selenium.webdriver import ActionChains


class InstaBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get("https://instagram.com")
        sleep(2)
        # Enter username
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        # Enter password
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        # Submit
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(4)
        # Skip pop-ups
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        sleep(4)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        sleep(2)

    def scrollFullPage(self):
        i = 1
        SCROLL_PAUSE_TIME = 2
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            if i > 2:
                break
            last_height = new_height
            i += 1
            j = 1
            sleep(2)

        # Scroll to top
        self.driver.execute_script("window.scrollTo(0, 0);")
        sleep(10)

 
    def openCaptions(self):
        i = 0
        while i < 50:
            moreButton = self.driver.find_element_by_class_name('sXUSN')
            self.driver.execute_script("arguments[0].scrollIntoView();", moreButton)
            sleep(2)
            self.driver.execute_script("window.scrollBy(0,-50);")
            sleep(2)
            moreButton.click()
            self.driver.execute_script("window.scrollBy(0,150);")
            sleep(2)
            i += 1

        



myBot = InstaBot("tkpaddles95@gmail.com", pw)
myBot.scrollFullPage()
myBot.openCaptions()